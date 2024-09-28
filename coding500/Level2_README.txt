//Welcome to the second level
//Time to add a new instruction: the 'BOH' statement
//A 'BOH' statement is composed by a COND and a list of INSTRUCTIONS.
//inside the BOH there could be an alternative, called OH, which have also its COND and instructions' list.
//Only one of them will be executed, but remember that the OH is not always present.
//
//RULES1: entire BOH statements lies always on a single line
//RULES2: CONDs are evaluated from LEFT TO RIGHT
//RULES3: each COND is always binary, and there are new operations for them (es. QE, EL, ...)
//
//BOH statements will always be on separated lines from different operations.

//BEGIN EXAMPLE1
N2m4m3Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN50a2s10QE BOH
//END EXAMPLE1: Prints 42

//BEGIN EXAMPLE2
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN50a2s10EL BOH
//END EXAMPLE2: Prints 42

//BEGIN EXAMPLE3
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN50a2s10TL BOH
//END EXAMPLE3: Prints 12

//BEGIN EXAMPLE4
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN50a2s10TG BOH
//END EXAMPLE4: Prints 12


//BEGIN EXAMPLE5
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN50a2s10EG BOH
//END EXAMPLE5: Prints 42

//BEGIN EXAMPLE6
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN1s1TG OR Vvrarrr1rN50a2s10TG BOH
//END EXAMPLE6: Prints 42

//BEGIN EXAMPLE7
N2m4m3d2Vvrarrr2r= N2a4m3d2s1m5a2Vvrarrr1r=
HOB HO Vvrarrr2rP | N1s1N1s1QE OH Vvrarrr1rP | Vvrarrr1rN1s1EN AND Vvrarrr1rN50a2s10TG BOH
//END EXAMPLE7: Prints 12

//BEGIN EXAMPLE8
N3m3Vvrarrr6r= N3m17Vvrarrr5r= N2m43Vvrarrr4r= 
HOB HO Vvrarrr5rN1s0ADDVvrarrr6r=  | Vvrarrr6rVvrarrr6rQE OH Vvrarrr3rN0a0m2a3ADDVvrarrr6r=  | Vvrarrr5rVvrarrr4rQE BOH 
Vvrarrr6rP
//END EXAMPLE8: Prints 52 

//BEGIN EXAMPLE9
BhbsbiblbgbnbebVvrarrr3r= BoblblbebhbVvrarrr2r= BobabibcbVvrarrr1r=
HOB HO Vvrarrr1rP  Vvrarrr1rBobdbnbobmbADDVvrarrr1r=  | Vvrarrr3rBnbabiblbabtbibQE OH Vvrarrr2rP  Vvrarrr2rBdblbrbobwbADDVvrarrr2r=  | Vvrarrr3rBhbsbiblbgbnbebQE BOH
//END EXAMPLE9: Prints "helloworld" 

//BEGIN EXAMPLE10
N1s0Vfrlrargr= 
HOB BhbobsbtbibtbubobhbtbibwbhbobbbebnboblbabrbobobpbabP  | VfrlrargrN1s0EN BOH 
//END EXAMPLE10: it doesn't print anything...

//BEGIN EXAMPLE11
N1a2m3Vfrlrargr= 
HOB BhbobsbtbibtbubobhbtbibwbhbobbbebnboblbabrbobobpbabP  | VfrlrargrN1s0EN BOH
//END EXAMPLE11: Prints "apooralonebohwithoutitsoh"
