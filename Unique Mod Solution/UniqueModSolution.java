import java.util.Scanner;
public class UniqueModSolution {

	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		int numberOfMods, uniqueMod = 1;
		int[] remainders;
		int[] mods;
		
		System.out.println("Please enter the number of mods you want:");
		
		do {
			numberOfMods = input.nextInt();
			
			if(numberOfMods < 2) {
				System.out.println("Please enter a number that's bigger than 1:");
			}
			
		} while(numberOfMods < 2);
		
		remainders = new int[numberOfMods];
		mods = new int[numberOfMods];
		
		for(int i = 0; i < numberOfMods; i++) {
			System.out.println("Please enter a positive mod number:");
			mods[i] = input.nextInt();
			uniqueMod *= mods[i];
			
			System.out.println("Please enter a remainder less than " + mods[i] + ":");
			
			do {
				remainders[i] = input.nextInt();
				
				if(remainders[i] >= mods[i]) {
					System.out.println("You didn't enter a remainder less than " + mods[i] + ":");
				}
				
			} while(remainders[i] >= mods[i]);
		}
		
		boolean match = false;
		for(int i = 1; i < uniqueMod + 1; i++) {
			match = true;
			
			for(int j = 0; j < mods.length; j++) {
				if(i % mods[j] != remainders[j]) {
					match = false;
				}
			}
			
			if(match) {
				System.out.println("Number that matches: " + i);
			}
		}
		
		if(!match) {
			System.out.println("No match");
		}
		
		input.close();
	}
}
