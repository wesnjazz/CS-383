Name: DongWon Park
Most favourite: Lecture 00 First lecture
Least favourite: Lecture 16 Machine learning
Worked with: Alone
Notes:
	I did Option #2 which is described in piazza post by Justin Payan

Original Post: @337
using the jaccard index for voting behavior
In general, the Jaccard index is used for problems that compare sets, and a few people have asked how to correctly apply it to the vectors of voting results we have for this assignment.  There are actually two ways to interpret Jaccard, and both are valid.  Consider the example below:
Person1: [ Yea, Nay, Yea, Nay, Nay ]
Person2: [ Yea, Nay, Yea, Yea, Present ]
(Option 1) Consider all of the votes, count the ones that agree, and divide by the total number of votes.  In this case, the denominator will be the same for all cases.  Here, Jaccard(Person1, Person2) = 3/5 = 0.6
(Option 2) Consider the sets created by votes relative to a particular value.  For example, compare the sets of bills that each person supported with a 'Yea' vote.  Jaccard(Person1, Person2) = 2/3 = 0.66
Either one will work for agglomerative clustering.  Make sure you document what you did in your readme.txt


