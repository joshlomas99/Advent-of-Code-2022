#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

void Day1() {
    // Create vector for elf sums and start the first elf at zero
    vector<int> elves;
    int sum{0};
    string line;
    ifstream myfile("../Inputs/Day1_Inputs.txt");
    // Read data from input file
    if (myfile.is_open())
    {
        while ( getline (myfile,line) )
        {
            // New lines indiciate a new elf
            if (line.length() == 0) {
                elves.push_back(sum);
                sum = 0;
            } else {
                // Else add the new calories to the current elf's total
                sum += stoi(line);
            }
        }
        myfile.close();
    } else {
        cout << "Unable to open file" << endl;
    }
    // Sort totals in ascending order
    sort(elves.begin(), elves.end());
    //#### Part 1 ####//
    // The final value in the sorted list is the maximum
    cout << "Part 1: " << elves.at(elves.size()-1) << endl;
    //#### Part 2 ####//
    // Add the final 3 values in the sorted list
    int highest_3_total = 0;
    for (int i = 1; i < 4; i++) {
        highest_3_total += elves.at(elves.size()-i);
    }
    cout << "Part 2: " << highest_3_total << endl;
}
