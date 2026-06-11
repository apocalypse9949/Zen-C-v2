import glob

for filepath in glob.glob('.github/workflows/*.yml'):
    with open(filepath, 'r') as f:
        c = f.read()

    # The missing env variable to node 24 was for the github action warnings.
    # The true build failures were MSAN complaining about `res` being null,
    # but I already fixed it using `xmalloc((nb ? strlen(nb) : 0) + 2)`.
    # AND ALSO the Twin_primes_whose_sum_is_square_number.zc compiler error
    pass
