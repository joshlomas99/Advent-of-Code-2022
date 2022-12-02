import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Day1 {
	public static void main(String[] args) {
		// Create list for elf sums and start the first elf at zero
		List<Integer> elves = new ArrayList<Integer>();
		int sum = 0;
		try {
			// Read data from input file
			File myObj = new File("Inputs/Day1_Inputs.txt");
			Scanner myReader = new Scanner(myObj);
			while (myReader.hasNextLine()) {
				String data = myReader.nextLine();
				// New lines indiciate a new elf
				if (data.length() == 0) {
					elves.add(sum);
					sum = 0;
				} else {
					// Else add the new calories to the current elf's total
					sum +=  Integer.parseInt(data);
				}
			}
			myReader.close();
		} catch (FileNotFoundException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
		// Sort totals in ascending order
		Collections.sort(elves);
		//#### Part 1 ####//
		// The final value in the sorted list is the maximum
		System.out.println("Part 1: " + elves.get(elves.size()-1));
		//#### Part 2 ####//
		// Add the final 3 values in the sorted list
		Integer highest_3_total = 0;
		for (int i = 1; i <= 3; i++) {
			highest_3_total += elves.get(elves.size()-i);
		}
		System.out.println("Part 2: " + highest_3_total);
	}
}
