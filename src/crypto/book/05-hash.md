# 5 - Hash Functions and Applications

Chapter Summery:

* Definitions:
    * Definition of collision-resistance.
    * Definition of second-preimage resistance.
    * Definition of preimage resistance.
    * Collision resistance implies second-preimage resistance.
    * Second-preimage resistance implies preimage resistance under uniformity assumption.
    * Collision resistance does not imply preimage resistance.
    * Preimage resistance does not imply collision resistance.
* Merkle-Damgard Transform:
    * Construction
    * Security
* Hash-and-MAC: Security proof
* Generic attacks:
    * Collision-resistance: O(1) space, O(2^l) time
    * Collision-resistance: O(2^(l/2)) space and time
    * Finding meaningful collisions
    * Markov chain for breaking collision-resistance: O(1) space and O(2^(l/2)) time
* Random oracle model
