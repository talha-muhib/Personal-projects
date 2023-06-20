import java.util.Arrays;

public class VigenereCipher {
	public void crackCipher(String s) {
		int key = getKey(s);
		int[] shifts = getShifts(s, key);
		String newString = "";
		
		for(int i = 0; i < s.length(); i++) {
			int charValue = ((int) s.charAt(i));
			charValue -= (shifts[i % key]);
			
			if(charValue < 65) {
				charValue = (91 - (65 - charValue));
			}
			
			char newChar = (char) charValue;
			newString += newChar;
		}
		
		System.out.println(Arrays.toString(shifts));
		System.out.println(newString);
	}
	
	private int[] getShifts(String s, int key) {
		int[] shifts = new int[key];
		
		for(int i = 0; i < key; i++) {
			String temp = "";
			for(int j = i; j < s.length(); j += key) {
				temp += s.charAt(j);
			}
			
			double q[] = frequency(temp);
			int shift = getShift(q);
			shifts[i] = shift;
		}
		
		return shifts;
	}
	
	private int getShift(double[] q) {
		double minimized = 1;
		int shiftValue = 0;
		
		double[] p = {
				0.085, 0.021, 0.045, 0.034, 0.112,
				0.018, 0.025, 0.030, 0.075, 0.002,
				0.011, 0.055, 0.030, 0.066, 0.072,
				0.032, 0.002, 0.076, 0.057, 0.070,
				0.036, 0.010, 0.013, 0.003, 0.018, 0.003
		};
		
		for(int i = 0; i < 26; i++) {
			double sum = 0;
			
			for(int j = 0; j < q.length; j++) {
				sum += (p[j] * q[j]);
			}
			
			if(Math.abs(0.065 - sum) < minimized) {
				minimized = Math.abs(0.065 - sum);
				shiftValue = i;
			}
			
			rotate(q);
		}
		
		return shiftValue;
	}
	
	private void rotate(double[] q) {
		double temp = q[0];
		for(int i = 0; i < q.length - 1; i++) {
			q[i] = q[i + 1];
		}
		
		q[q.length - 1] = temp;
	}
	
	private int getKey(String s) {
		double minimized = 1;
		int key = 0;
		
		for(int i = 1; i < 11; i++) {
			String temp = "";
			
			for(int j = 0; j < s.length(); j += i) {
				temp += s.charAt(j);
			}
			
			double freqs[] = frequency(temp);
			double f = sumSquares(freqs);
			
			if(Math.abs(0.065 - f) < minimized) {
				minimized = Math.abs(0.065 - f);
				key = i;
			}
		}
		
		return key;
	}
	
	private double[] frequency(String s) {
		double[] freqs = new double[26];
		
		for(int i = 0; i < 26; i++) {
			double count = 0;
			char c = ((char)(i + 65));
			
			for(int j = 0; j < s.length(); j++) {
				if(s.charAt(j) == c) {
					count++;
				}
			}
			
			freqs[i] = count/s.length();
		}
		
		return freqs;
	}
	
	private double sumSquares(double[] freqs) {
		double sum = 0;
		
		for(int i = 0; i < 26; i++) {
			double q = freqs[i];
			sum += (q * q);
		}
		
		return sum;
	}
	
	public static void main(String[] args) {
		VigenereCipher v = new VigenereCipher();
		v.crackCipher("WCTMNSGCYKVLQPTYTUMLIWIRGBWUKDLNJSWFKXKOTMSBGCMLCRYPTIXMRKVIAYYPEKVBQXXUCX"
				+ "XRQPYKDVIYTYYLFSRWQEVNQMOCVDSDKXHACCLDQBXFGZEPMSREOOXCTKRBFYRRJKZCVRIAQBVCEDTY"
				+ "AWILVKTNKXWRCVPCFYRWQEVNJYRCYOPJVRMLMMEPGPYJNIFCHYVCTEWFKXKRQCGYPDLCRKCKGXXOTM"
				+ "SBGCXSEUSLVRIQKNIMHDLCOOXCTSXKCIACNVFCCXERVOQNVLCDTKYBUDIPUDSNJSWFAYYPHSRYPMMY"
				+ "NSRDQBQYVSSLRYPGEOEPGGEPPSREVRERVRIWJKZCFSWAQFIPGNFMIEWOTMSBGCWRWMOMPDSNWLPGEZ"
				+ "EPMSREOOXCTCEATYWQCEWRKXXCZKWYESXWYRIPGZEPMSREOOXCTCHMPDHGUZPYAAVAQNIQCXHMPVCY"
				+ "EMINVZEWOORRXSEAQSRQEKVBUYVYUWEPVZLMPOENRCSUJKXFCZTCPCMDXSWGVYVQVYXFGMMRAYVRJY"
				+ "WCKXEPWCLUJYEPGXSRUEWNKMMMWCWGOZPWUMELVRIZQQYQSBGMFOAGVRSSVDLGPUMLIDLCSBGMFOWD"
				+ "QERBDIESUDMLRYPGEOHCRKVROORRFSVCEDIBWXWSUZIAVSREWCIPUDSYHBESFEPCPDACDCMRGGLGER"
				+ "AMWVHYUUJMTZEWOORRFOXYKVWUKDLRJOJYNCINTYQGUOXFCDXFGSVNCBOGPQWCUCMMPGSSNNFCRKMB"
				+ "HYVRJOGGVISDCEWRKXGFGMOCFSXQRKVIKXKKGDIPUKJRGBFCKXKLQDMDKOHMHKWGOSPYTAVAQNIQEK"
				+ "QZAYJDKMMYNCMLUKRYPDSLKYXFGILYFNMQEYZCTOHMXOVNCBOGPQQCVOVQUSQGNKVJACXGEUIPGNML"
				+ "NKXCFOGCOLIPNDQYTMYQDYSRJYJQCXELVYRGQZSJKMIBGZEPVWILVDSJFBINQBXCTCXFCDXFGGIZRK"
				+ "KCRBIRGXHCFDSYEMINVZEWOORRHYVRJOTYTUMLICIQUSSLDEXRJKXKQXIWGXHCFETGPDLCJKRBUYJQ"
				+ "EKQKGBWPCDLCTDLYPSRRJOGGVIWAQPJCTCMLURSPVSXQPYXHWCXACBHPKFIPUGLMCBIRJOZGEDMKUY"
				+ "JRJOJRDEXRJOGGVIXMQSXQPYXIPYALYRIRJOVRJOERVKGIUWSSPDIBCQEGPCXNCBOGPQQCVOVQKXXF"
				+ "GDAMESXGGCEPGMSLPOGRGNSPVRIUQBOMHMSNAMERULYREVIYTVCGVCRMVKHGHPMAWVXQEKQDQBSRJO"
				+ "VETYYNUDSPGZPGEKXCKXSRJOVYOOVGEKRAKDMCUYVGPNICFOPQGGLCTOMLVRIUQBPBCCEAQXWCSEIL"
				+ "EOCMWWMEJDFCYSWCTZEWKXKDQBCMWBTYTUMLIWIRGBAGVRGYURSPXSERJOENRBSNTSERGCQYTDTFQX"
				+ "IYRZESVRSPKDMCUKVCGXGMWBEEKXKYPISLGGLMDOPGGFIQVRERVRIWOSKFVRETGLICPCGYOWIBDIXF"
				+ "GPVYWNYJGXXNCBOGPQQCVOVOTMSBGCXMHSPCCZSJKMIPGZSPVKRBKXJMTWXFGSVNCIQCPDGYTNMQUE"
				+ "IPKWQCFSERGVCKGKRUJSPCKPCMWCICUYQCQXIRCWTCTSREYSXFCZEPMSREOOXCTGLMKCRMVKFYFQIB"
				+ "ESXWGWTJQIICFYXFGBMEJDXFKXKYPNGYNVXFGZSJKMI");
	}
}
