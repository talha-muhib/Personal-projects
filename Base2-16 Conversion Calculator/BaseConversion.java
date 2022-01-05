import java.util.Scanner;

public class BaseConversion {
	private static char[] arr = {'0', '1', '2', '3', '4', '5', '6', '7', '8',
			'9', 'A', 'B', 'C', 'D', 'E', 'F'};
	
	private String checkDigits(char digit) {
		for(int i = 0; i < arr.length; i++) {
			if(arr[i] == digit) {
				return Integer.toString(i);
			}
		}
		
		return null;
	}
	
	public int isValidSet(String number) {
		int properBase = 0;
		
		for(int i = 0; i < number.length(); i++) {
			String check = checkDigits(number.charAt(i));
			
			if(check == null) {
				return -1;
			}
			
			if(Integer.parseInt(check) >= properBase) {
				properBase = Integer.parseInt(check) + 1;
			}
		}
		
		return properBase;
	}
	
	public int convertToBase10(String number, int base) {
		int converted = 0, count = 0, digit;
		String display = "", check, data;
		
		for(int i = number.length() - 1; i > -1; i--) {
			check = checkDigits(number.charAt(count));
			digit = Integer.parseInt(check);
			converted += (digit * Math.pow(base, i));
			data = "(" + digit + " * " + base + "^" + i + ")";
			display += (display.isEmpty()) ? data : " + " + data;
			count++;
		}
		
		display += " = " + converted;
		System.out.println(display);
		
		return converted;
	}
	
	public String convertFromBase10(String integer, int base) {
		String newBase = "";
		int number = Integer.parseInt(integer), modulus, temp;
		
		if(number == 0) {
			return Integer.toString(0);
		}
		
		while(number > 0) {
			modulus = number % base;
			temp = number;
			number /= base;
			newBase = arr[modulus] + newBase;
			System.out.println(temp + " = " + number 
					+ " * " + base + " + " + modulus);
		}
		
		return newBase;
	}
	
	public static void main(String[] args) {
		BaseConversion BC = new BaseConversion();
		Scanner input = new Scanner(System.in);
		int fromBase = 16, converted = 0;
		String newBase = "";
		
		System.out.println("Type a positive number:");
		String number = input.next().toUpperCase();
		int minBase = BC.isValidSet(number);
		
		while(minBase == -1) {
			System.out.println("Invalid number. Try again:");
			number = input.next();
			minBase = BC.isValidSet(number);
		}
		
		if(minBase < 16) {
			System.out.println("What base is it in? "
					+ "Enter a base between " + minBase + " and 16 (Inclusive):");
			fromBase = input.nextInt();
			
			while(fromBase < minBase || fromBase > 16) {
				System.out.println("Invalid base. Try again:");
				fromBase = input.nextInt();
			}
		}
		
		System.out.println("What base are you converting it to?");
		int toBase = input.nextInt();
		
		while(toBase < 2 || toBase > 16) {
			System.out.println("Invalid base. Try again:");
			toBase = input.nextInt();
		}
		
		if(fromBase == 10) {
			newBase = BC.convertFromBase10(number, toBase);
		} else {
			if(toBase == 10) {
				converted = BC.convertToBase10(number, fromBase);
				newBase = Integer.toString(converted);
			} else {
				converted = BC.convertToBase10(number, fromBase);
				newBase = BC.convertFromBase10(Integer.toString(converted), toBase);
			}
		}
		
		System.out.println("\n" + number + "_" + fromBase + 
				" to " + newBase + "_" + toBase);
		
		input.close();
	}
}
