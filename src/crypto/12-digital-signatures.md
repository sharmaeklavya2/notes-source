# 12 - Digital Signature Schemes

* Definition of a digital signature scheme as the triple (Gen, Sign, Verify).
* euf-cma experiment and security.
* hash-and-sign: definition and proof of security.
* RSA signatures:
    * Plain RSA:
        * no-message attack
        * targeted forgery
    * RSA-FDH:
        * definition
        * necessary conditions on H
        * proof of security in the random-oracle model
        * need for FDH to have large enough range
* Discrete-log signatures:
    * Identification schemes:
        * Definition
        * Non-degeneracy
        * Security
    * Fiat-Shamir transform:
        * definition
        * proof of security
    * Schnorr identification scheme:
        * definition
        * proof of security
    * \* DSA and ECDSA
* \* Signatures from Hash-functions:
    * Lamport's signature
    * Chain-based
    * Tree-based
* \* Certificates and public-key infrastructures
* \* SSL-TLS
* \* Signcryption
