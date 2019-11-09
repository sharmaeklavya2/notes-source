# 11 - Public-Key Encryption

* Need for securely distributing public keys.
* Definition of a public-key encryption scheme as the triple (Gen, Enc, Dec).
* ind-cpa experiment and cpa security.
* Impossibility of perfectly secret public-key encryption schemes.
* Insecurity of deterministic encryption schemes.
* mult-cpa security:
    * ind-mult-cpa experiment and mult-cpa security.
    * encrypting arbitrary length messages using ind-mult-cpa secure scheme.
    * \* Proof that cpa security implies mult-cpa security.
* ind-cca experiment and security.
* hybrid encryption and kem-dem paradigm:
    * definition of KEM as triple (Gen, Encaps, Decaps) and DEM as a private-key encryption scheme.
    * hybrid encryption using KEM+DEM.
    * cpa-security of KEMs.
    * proof of cpa-security of hybrid encryption scheme.
    * cca-security of KEMs.
    * proof of cca-security of hybrid encryption scheme.
* ElGamal encryption scheme:
    * definition.
    * proof that DDH is hard implies ElGamal is cpa-secure.
    * Hashed ElGamal for KEM.
    * proof that CDH is hard implies Hashed ElGamal is a secure KEM.
    * chosen-ciphertext attack on ElGamal.
* RSA encryption:
    * Textbook RSA encryption.
    * Real-life attacks on textbook RSA:
        * quadratic improvement in recovering m
        * encrypting small messages using short e
        * encrypting a partially known message
        * encrypting related messages
        * sending same message to multiple receivers
    * \* Padded RSA and PKCS #1 v1.5
    * \* CPA-secure encryption without random-oracles
    * \* OEAP and RSA PKCS #1 v2.0
    * CCA-secure KEM in random-oracle model
    * RSA implementation issues:
        * Fault attack on chinese remaindering
        * Dependent public keys
        * Dependent public keys where users trust each other
        * Randomness quality in RSA keygen
