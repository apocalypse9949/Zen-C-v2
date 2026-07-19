// SPDX-License-Identifier: MIT
#include "../arena.h"
#include "symbols.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

Scope *symbol_scope_create(Scope *parent, const char *name)
{
    Scope *s = xmalloc(sizeof(Scope));
    memset(s, 0, sizeof(Scope));
    s->parent = parent;
    if (name)
    {
        s->name = xstrdup(name);
    }
    s->hash_size = 32;
    s->hash_count = 0;
    s->hash_table = xmalloc((size_t)s->hash_size * sizeof(*s->hash_table));
    memset(s->hash_table, 0, (size_t)s->hash_size * sizeof(*s->hash_table));
    return s;
}

void symbol_scope_free(Scope *s)
{
    if (!s)
    {
        return;
    }

    ZenSymbol *sym = s->symbols;
    while (sym)
    {
        ZenSymbol *next = sym->next;
        if (sym->name)
        {
            zfree(sym->name);
        }
        if (sym->cfg_condition)
        {
            zfree(sym->cfg_condition);
        }

        if (sym->kind == SYM_ALIAS)
        {
            if (sym->data.alias.original_type)
            {
                zfree(sym->data.alias.original_type);
            }
        }
        else if (sym->kind == SYM_CONSTANT)
        {
            if (sym->data.constant.str_val)
            {
                zfree(sym->data.constant.str_val);
            }
        }
        else if (sym->kind == SYM_MODULE)
        {
            if (sym->data.module.path)
            {
                zfree(sym->data.module.path);
            }
            if (sym->data.module.alias_name)
            {
                zfree(sym->data.module.alias_name);
            }
        }

        zfree(sym);
        sym = next;
    }

    if (s->name)
    {
        zfree(s->name);
    }
    if (s->hash_table)
    {
        zfree(s->hash_table);
    }
    zfree(s);
}

static unsigned int hash_str(const char *str)
{
    unsigned int h = 2166136261u;
    while (*str)
    {
        h ^= (unsigned char)*str++;
        h *= 16777619u;
    }
    return h;
}

static void rehash_scope(Scope *s)
{
    int old_size = s->hash_size;
    int new_size = old_size * 2;
    void *old_table_void = s->hash_table;
    struct
    {
        const char *name;
        ZenSymbol *sym;
    } *old_table = old_table_void;
    s->hash_table = xmalloc((size_t)new_size * sizeof(*s->hash_table));
    memset(s->hash_table, 0, (size_t)new_size * sizeof(*s->hash_table));
    s->hash_size = new_size;

    for (int i = 0; i < old_size; i++)
    {
        if (old_table[i].name)
        {
            unsigned int idx = hash_str(old_table[i].name) & (unsigned int)(new_size - 1);
            for (int j = 0; j < new_size; j++)
            {
                unsigned int slot = (idx + (unsigned int)j) & (unsigned int)(new_size - 1);
                if (!s->hash_table[slot].name)
                {
                    s->hash_table[slot].name = old_table[i].name;
                    s->hash_table[slot].sym = old_table[i].sym;
                    break;
                }
            }
        }
    }
    zfree(old_table);
}

static void hash_insert(Scope *s, const char *name, ZenSymbol *sym)
{
    if (s->hash_count >= s->hash_size / 2)
    {
        rehash_scope(s);
    }
    unsigned int idx = hash_str(name) & (unsigned int)(s->hash_size - 1);
    for (int i = 0; i < s->hash_size; i++)
    {
        unsigned int slot = (idx + (unsigned int)i) & (unsigned int)(s->hash_size - 1);
        if (!s->hash_table[slot].name)
        {
            s->hash_table[slot].name = name; // sym->name
            s->hash_table[slot].sym = sym;
            s->hash_count++;
            return;
        }
        if (strcmp(s->hash_table[slot].name, name) == 0)
        {
            // Update existing or chain? For symbol table, we typically don't have dupes, but if we
            // do, we should probably allow list traversal. Let's just push to head of list but keep
            // hash to the first one seen. Actually, symbol_add pushes to head, so newer symbols
            // shadow older ones. So we update the hash table.
            s->hash_table[slot].sym = sym;
            return;
        }
    }
}

ZenSymbol *symbol_add(Scope *s, const char *name, SymbolKind kind)
{
    if (!s || !name)
    {
        return NULL;
    }

    ZenSymbol *sym = xmalloc(sizeof(ZenSymbol));
    memset(sym, 0, sizeof(ZenSymbol));
    sym->name = xstrdup(name);
    sym->kind = kind;

    sym->next = s->symbols;
    s->symbols = sym;

    hash_insert(s, sym->name, sym);

    return sym;
}

ZenSymbol *symbol_lookup_local(Scope *s, const char *name)
{
    if (!s || !name)
    {
        return NULL;
    }

    if (s->hash_table)
    {
        unsigned int idx = hash_str(name) & (unsigned int)(s->hash_size - 1);
        for (int i = 0; i < s->hash_size; i++)
        {
            unsigned int slot = (idx + (unsigned int)i) & (unsigned int)(s->hash_size - 1);
            if (!s->hash_table[slot].name)
            {
                return NULL;
            }
            if (s->hash_table[slot].name[0] == name[0] &&
                strcmp(s->hash_table[slot].name, name) == 0)
            {
                return s->hash_table[slot].sym;
            }
        }
    }

    ZenSymbol *curr = s->symbols;
    while (curr)
    {
        if (curr->name && curr->name[0] == name[0] && strcmp(curr->name, name) == 0)
        {
            return curr;
        }
        curr = curr->next;
    }
    return NULL;
}

ZenSymbol *symbol_lookup(Scope *s, const char *name)
{
    if (!name)
    {
        return NULL;
    }

    Scope *curr_scope = s;
    while (curr_scope)
    {
        ZenSymbol *sym = symbol_lookup_local(curr_scope, name);
        if (sym)
        {
            return sym;
        }
        curr_scope = curr_scope->parent;
    }
    return NULL;
}

ZenSymbol *symbol_lookup_kind(Scope *s, const char *name, SymbolKind kind)
{
    if (!name)
    {
        return NULL;
    }

    Scope *curr_scope = s;
    while (curr_scope)
    {
        if (curr_scope->hash_table)
        {
            unsigned int idx = hash_str(name) & (unsigned int)(curr_scope->hash_size - 1);
            for (int i = 0; i < curr_scope->hash_size; i++)
            {
                unsigned int slot =
                    (idx + (unsigned int)i) & (unsigned int)(curr_scope->hash_size - 1);
                if (!curr_scope->hash_table[slot].name)
                {
                    break;
                }
                if (curr_scope->hash_table[slot].name[0] == name[0] &&
                    strcmp(curr_scope->hash_table[slot].name, name) == 0)
                {
                    // Due to shadowing and same-name diff-kind symbols, we might need to traverse
                    // from this symbol if kind mismatch, but typically we don't allow same name in
                    // same scope unless they are different namespaces. Actually, to be safe, just
                    // fall back to linear search or traverse the linked list. In Zen, a symbol name
                    // is generally unique per scope. Let's just traverse the symbol list to be 100%
                    // correct.
                    ZenSymbol *sym = curr_scope->hash_table[slot].sym;
                    while (sym && (!sym->name || strcmp(sym->name, name) != 0))
                    {
                        // The hash table points to the latest. If it's a match, great.
                        // If we need kind match, the linked list is better if there's multiple with
                        // same name.
                        sym = sym->next;
                    }
                    if (sym && sym->kind == kind && strcmp(sym->name, name) == 0)
                    {
                        return sym;
                    }
                }
            }
        }

        ZenSymbol *sym = curr_scope->symbols;
        while (sym)
        {
            if (sym->kind == kind && sym->name && sym->name[0] == name[0] &&
                strcmp(sym->name, name) == 0)
            {
                return sym;
            }
            sym = sym->next;
        }
        curr_scope = curr_scope->parent;
    }
    return NULL;
}
