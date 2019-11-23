# 4 - Message Authentication Codes

Chapter Summary:

* MAC:
    * Definition of MAC, canonical verification, correctness.
    * Definition of experiment `Mac-forge`, CMA security, CMVA security.
    * Definition of experiment `Mac-sforge`, strong CMA security, strong CMVA security.
    * Timing attack on MAC and how to mitigate it.
    * Constructing MAC from PRF and proof of security.
    * Domain extension for MAC and proof of security.
    * Definition of CBC-MAC (security proof is optional).
* Authenticated Encryption:
    * Definition of `Enc-forge` (ciphertext integrity experiment) and unforgeability.
    * Attack on 'encrypt-and-authenticate'.
    * Attack on 'authenticate-then-encrypt'.
    * Prove that 'encrypt-then-authenticate' is secure and unforgeable.
    * Attack on 'encrypt-then-authenticate' when same key is used for encryption and mac.
    * Prove that authenticated encryption is CCA-secure.
* Information-theoretic MAC:
    * Definition of perfect 1-time unforgeability.
    * Construct perfect MAC using strongly-universal function.
    * Construct strongly universal function using fields.
    * Prove min key length for perfect unforgeability.
