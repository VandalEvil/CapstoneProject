# DataStructuresAndAlgorithms

**What was the problem you were solving in the projects for this course?**

In this course we explored a few data structures and evaluated their efficiency in different scenarios. We began with vector and arrays and moved on to hash tables and binary search trees. Each week we worked on one of the structures and applied it through c++ labs. The ultimate project for the course was to determine the best data structure for the following scenario:

A college called ABCU has engaged us to write a program that can store, sort, output their course curriculum. We have to determine the best data structure for the job and implement it in c++.

**How did you approach the problem?**

For project 1 we did an analysis on algorithm efficiency for various operations of our program based on pseudocode we wrote for each data structure. This analysis, combined with the criteria for the program, allowed us to see that the best data structure for this would be a binary search tree (a hash table is more efficient at a couple of functions, but is unsuitable for printing a sorted list, which is something the program needed to do well).

**How did you overcome any roadblocks you encountered while going through the activities or project?**

I didn't have too much trouble; nothing I couldn't work out on my own or by focusing on my previous work. I spend a lot of time writing code examples to familiarize myself with them and give me notes to look back on. A requirement of the course objects was that if they contained a prerequisite, that prerequisite had to exist as a course in the curriculum, otherwise we would not create that course object. This was the trickiest part of the logic, one that has many potential solutions...I chose to make a binary tree from all the course IDs first, then as I added course objects to my main data structure, I ran a search through that tree before adding prerequisites and calling my constructor.

**How has your work on this project expanded your approach to designing software and developing programs?**

As a beginner programmer, most of the projects I have worked on have not had enough complexity to warrant implementing a data structure outside of a basic vector or array. Knowing my way around some efficient means of data storage and manipulation is vital to my future programming.

**How has your work on this project evolved the way you write programs that are maintainable, readable, and adaptable?**

Every additional project I work on on my way to a career in software development makes me a little more proficient and a little more knowledgable. This project felt like a huge leap from where I was two months ago.
