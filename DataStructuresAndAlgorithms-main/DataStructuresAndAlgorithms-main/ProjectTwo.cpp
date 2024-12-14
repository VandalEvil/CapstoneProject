// Project     : ProjectTwo.cpp
// Author      : Buddy Marcey
// Course      : CS300 DSA
// Date        : October 15, 2023
// Version     : 1.0
// Description : ABCU Course Manager



#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

// Object construction for courses

struct Course {

	// Components, with unique courseID
	std::string courseID;
	std::string courseName;
	std::vector<std::string> prerequisites;

	// Default constructor
	Course() {
		courseID = "None";
		courseName = "None";
	}

	// Overloaded constructor with up to three prerequisites
	Course(std::string t_courseID, std::string t_courseName, 
		std::string t_prerequisite1, std::string t_prerequisite2,
		std::string t_prerequisite3) {
		courseID = t_courseID;
		courseName = t_courseName;
		prerequisites.push_back(t_prerequisite1);
		prerequisites.push_back(t_prerequisite2);
		prerequisites.push_back(t_prerequisite3);
	}
};

// Node constructor for building BST nodes

struct Node {
	Course course;
	Node* left;
	Node* right;

	// Default constructor
	Node() {
		left = nullptr;
		right = nullptr;
	}

	// Overloaded constructor passing in a course object
	Node(Course t_course) :
		Node() {
		course = t_course;
	}
};

// BST class declaration and all required functions
// InOrder with inOrder print list in order
// Insert with addNode insert nodes into BST, used in file load
// Two versions of print functions, one with prerequisites and one without
// Search function for single print and for validation check

class BinarySearchTree {
private:
	Node* root;

	void inOrder(Node* t_node);
	void addNode(Node* t_node, Course t_course);

public:
	BinarySearchTree();
	virtual ~BinarySearchTree();
	void InOrder();
	void Insert(Course t_course);
	void printCourse(Course t_course);
	void printAllCoursesFormat(Course t_course);
	Course Search(std::string t_courseID);
};

// default constructor for initializing a BST

BinarySearchTree::BinarySearchTree() {
	root = nullptr;
}

// Destructor declared but not defined or called anywhere.
// Perhaps the prereqCheck BST should be destructed to free up
// memory after the input is finished, but that is not part of 
// this assignment.

BinarySearchTree::~BinarySearchTree() {

}

// Initializes the print in order function starting at root

void BinarySearchTree::InOrder() {

	this->inOrder(root);
}

// Recursive function for printing the BST in order

void BinarySearchTree::inOrder(Node* t_node) {

	if (t_node != nullptr) {
		inOrder(t_node->left);
		printAllCoursesFormat(t_node->course);
		inOrder(t_node->right);
	}
}

// Initializes insertion function to add node to BST
// or creates first node at root if BST is empty

void BinarySearchTree::Insert(Course t_course) {
	if (root == nullptr) {
		root = new Node(t_course);
	}
	else {
		this->addNode(root, t_course);
	}
}

// Recursive function that places new node in the proper
// place in the tree, effectively sorting as it goes

void BinarySearchTree::addNode(Node* t_node, Course t_course) {

	// Determine if function should go left or right
	if (t_node->course.courseID.compare(t_course.courseID) > 0) {

		// continue searching left until a spot is open
		if (t_node->left == nullptr) {
			t_node->left = new Node(t_course);
		}
		else {
			this->addNode(t_node->left, t_course);
		}
	}

	// continue searching right until an a spot is open
	else {
		if (t_node->right == nullptr) {
			t_node->right = new Node(t_course);
		}
		else {
			this->addNode(t_node->right, t_course);
		}
	}
}

// function to print a course along with its prerequisites
// used with search for switch case 3

void BinarySearchTree::printCourse(Course t_course) {
	std::cout << t_course.courseID << ", " << t_course.courseName
		<< std::endl << "Prerequisites: ";
	for (int i = 0; i < t_course.prerequisites.size(); ++i) {
		if (i == t_course.prerequisites.size() - 1) {
			std::cout << t_course.prerequisites[i];
		}
		else {
			std::cout << t_course.prerequisites[i] << ", ";
		}
	}
	std::cout << std::endl;
}

// print function to print just the name and ID of all courses 
// in the BST, used for switch case 2

void BinarySearchTree::printAllCoursesFormat(Course t_course) {
	std::cout << t_course.courseID << ", " << t_course.courseName << std::endl;
}

// Search for courseID, used for validation and for print single course

Course BinarySearchTree::Search(std::string t_courseID) {
	Node* current = root;

	while (current != nullptr) {
		if (current->course.courseID.compare(t_courseID) == 0) {
			return current->course;
		}
		else if (t_courseID.compare(current->course.courseID) < 0) {
			current = current->left;
		}
		else {
			current = current->right;
		}
	}

	// if no course found, return default course, whose ID is "None" by default
	Course course;
	return course;
}

// function to load data file and turn lines into course
// object, tied to nodes to form a BST

void loadCourses(std::string t_fileName, BinarySearchTree* t_bst, BinarySearchTree* t_bstValidation) {

	// opens input file passed by user
	std::ifstream inputFile(t_fileName);
	std::string line;
	bool valid = true;

	// keeps track of how many courses have been added
	int numCourses = 0;

	if (inputFile.is_open()) {

		// get line from input file
		while (std::getline(inputFile, line)) {

			//split into tokens and add to tempVector
			std::stringstream splitLine(line);
			std::string token;
			std::vector<std::string> tempVector;
			bool valid = true;
			while (std::getline(splitLine, token, ',')) {
				if (token != "") {
					tempVector.push_back(token);
				}
			}

			// if tempVector.size() is less than 2, line is invalid
			if (tempVector.size() >= 2) {
				Course courseToBuild;
				courseToBuild.courseID = tempVector[0];
				courseToBuild.courseName = tempVector[1];
				
				// if tempVector.size() is 3 or greater, then prerequisites exist
				if (tempVector.size() >= 3) {
					for (int i = 2; i < tempVector.size(); i++) {

						// check to make sure prerequisites exist as courses in the passed BST
						if ((t_bstValidation->Search(tempVector[i]).courseID == "None")) {
							valid = false;
						} else {
							courseToBuild.prerequisites.push_back(tempVector[i]);
						}
					}
				}

				// add to BST, unless prerequisite causes invalid state
				if (valid) {
					t_bst->Insert(courseToBuild);
					numCourses++;
				}
			}
		}

		inputFile.close();
	}
	else {
		std::cout << "Unable to open file" << std::endl;
	}

	// write count of courses loaded
	std::cout << "Number of courses loaded: " << numCourses << std::endl;
}

// function to build the BST for prerequisite validation check

void loadPrerequisites(std::string t_filename, BinarySearchTree* t_bst) {

	// Open file and build a BST that contains just the courseIDs
	// so that we can use that to search for validation for the main BST
	std::ifstream inputFile(t_filename);
	std::string line;
	if (inputFile.is_open()) {
		while (std::getline(inputFile, line)) {
			std::stringstream splitLine(line);
			std::string token;
			std::vector<std::string> tempVector;
			while (std::getline(splitLine, token, ',')) {
				if (token != "") {
					tempVector.push_back(token);
				}
			}
			Course courseCheck;
			courseCheck.courseID = tempVector[0];
			t_bst->Insert(courseCheck);
		}

		inputFile.close();
	}
}

// function to display the menu options, returns choice

char displayMenu() {
	char userOption = '0';
	std::cout << std::endl;
	std::cout << "\n1. Load Data Structure." << std::endl;
	std::cout << "2. Print Course List." << std::endl;
	std::cout << "3. Print Course." << std::endl;
	std::cout << "9. Exit." << std::endl;
	std::cout << "\nWhat would you like to do? ";
	std::cin >> userOption;
	return userOption;
}


int main() {

	// initialize main BST to hold data
	BinarySearchTree* bst;
	bst = new BinarySearchTree();

	// initialize BST to hold courseIDs for validation
	BinarySearchTree* prereqCheck;
	prereqCheck = new BinarySearchTree();
	
	// declare variables for various functions
	char currentOption = '0';
	std::string searchValue = "";
	std::string userFileName = "";
	bool loaded = false;
	
	std::cout << "\nWelcome to the Course Planner." << std::endl;
	while (currentOption != '9') {
		char currentOption = displayMenu();
		switch (currentOption) {
		case '1':
			// load stuff
			std::cout << "Enter File to Import:" << std::endl;
			std::cin >> userFileName;
			loadPrerequisites(userFileName, prereqCheck);
			loadCourses(userFileName, bst, prereqCheck);
			loaded = true;
			
			break;

		case '2':
			// Print the whole list
			if (loaded) {
				bst->InOrder();
			}
			else {
				std::cout << "No courses have been loaded." << std::endl;
			}
			
			break;

		case '3':
			// Print one course by prompt
			if (loaded) {
				std::cout << "Which course would you like to print?" << std::endl;
				std::cin.ignore();
				std::getline(std::cin, searchValue);
				std::cout << std::endl;
				for (int i = 0; i < searchValue.size(); i++) {
					searchValue.at(i) = std::toupper(searchValue.at(i));
				}
				bst->printCourse(bst->Search(searchValue));
			}
			else {
				std::cout << "No courses have been loaded." << std::endl;
			}
			
			break;

		case '9':
			// exit program
			std::cout << "Thank you for using the Course Planner!" << std::endl;
			exit(0);
			break;

		default:
			// basic switch case input validation
			std::cout << currentOption << " is not a valid option.";
			std::cin.ignore();
			break;
			
		}
	}

	return 0;
}