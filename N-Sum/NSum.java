import java.util.ArrayList;
import java.util.Scanner;

public class NSum {
	/**Finding sum using 2 elements of a sorted array*/
	private ArrayList<Integer> twoSum(int[] arr, int sum, int l, int r, ArrayList<Integer> list) {
		while(l < r) {
			int arraySum = arr[l] + arr[r];
			
			if(arraySum == sum) {
				list.add(arr[l]);
				list.add(arr[r]);
				return list;
			} else if(arraySum < sum) {
				l++;
			} else {
				r--;
			}
		}
		
		return list;
	}
	
	/**Standard binary search algorithm*/
	private ArrayList<Integer> binarySearch(int[] arr, int sum, ArrayList<Integer> list) {
		int l = 0, r = arr.length - 1;
		
		while(l <= r) {
			int mid = (l + r)/2;
			
			if(arr[mid] == sum) {
				list.add(sum);
				return list;
			} else if(arr[mid] < sum) {
				l = mid + 1;
			} else {
				r = mid - 1;
			}
		}
		
		return list;
	}
	
	/**Finding a sum using n elements of an array*/
	public ArrayList<Integer> nSum(int[] arr, int sum, int n, int index, ArrayList<Integer> list) {
		if(arr.length < n || n < 1) {
			return list;
		} else if(n == 1) {
			return binarySearch(arr, sum, list);
		} else if(n == 2) {
			return twoSum(arr, sum, index, arr.length - 1, list);
		} else {
			for(int i = index; i < arr.length - (n - 1); i++) {
				if(!nSum(arr, sum - arr[i], n - 1, i + 1, list).isEmpty()) {
					list.add(arr[i]);
					return list;
				}
			}
			
			return list;
		}
	}
	
	/**O(n) sorting algorithm (not in-place)*/
	public void linearSort(int[] arr) {
		int max = Integer.MIN_VALUE, min = Integer.MAX_VALUE, count = 0;
		int[] tempArr;
		
		for(int i = 0; i < arr.length; i++) {
			if(max < arr[i]) {
				max = arr[i];
			}
			
			if(min > arr[i]) {
				min = arr[i];
			}
		}
		
		int finalMax = Math.max(max, Math.abs(min));
		int shift = (min < 0) ? Math.abs(min) : 0;
		int shiftLength;
		
		if(min < 0 && max >= Math.abs(min)) {
			shiftLength = finalMax + 1 + Math.abs(min);
		} else if(min < 0 && max < Math.abs(min)) {
			shiftLength = finalMax + 1 + max;
		} else {
			shiftLength = finalMax + 1;
		}
		
		tempArr = new int[shiftLength];
		
		for(int i = 0; i < arr.length; i++) {
			tempArr[arr[i] + shift]++;
		}
		
		for(int i = 0; i < tempArr.length; i++) {
			while((tempArr[i]--) > 0) {
				arr[count++] = i - shift;
			}
		}
	}
	
	//Test run
	public static void main(String[] args) {
		NSum findN = new NSum();
		Scanner input = new Scanner(System.in);
		
		int[] A = {90, 16, 100, 102, 6, 5, 8, 9, -6, -7, -54, 71};
		ArrayList<Integer> list = new ArrayList<>();
		
		System.out.println("Enter a target sum:");
		int target = input.nextInt();
		
		int n;
		do {
			System.out.println("For n enter a number between 1 and " + A.length + ":");
			n = input.nextInt();
		} while (n < 1 || n > A.length);
		
		findN.linearSort(A);
		System.out.println(findN.nSum(A, target, n, 0, list));
		
		input.close();
	}
}
