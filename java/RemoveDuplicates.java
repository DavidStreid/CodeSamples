import java.util.Random;
import java.util.Arrays;

public class RemoveDuplicates{
	private static Random random = new Random();

	private static int[] makeArr(int n, int max){
		int[] arr = new int[n];
		for(int i = 0; i< n; i++){
			arr[i] = random.nextInt(max);
		}
		return arr;
	}

	private static void removeDuplicates(int[] arr){
		int i = 0;		// iterates through list
		int j = 0;		// Marks (inclusive) end of unique elements

		while(i < arr.length-1){
			// Loop until next unique element is reached
			while(arr[i] == arr[j] && i < arr.length-1){
				i++;		
			}
			// Next unique element was found before reaching list's end
			if(i<arr.length){
				j++;					// Make room in arr[:j] for new unique
				arr[j] = arr[i];		// Add new unique element
			}
		}
		// Replace rest of list consisting of duplicates w/ 0s
		while(j<arr.length){
			arr[j] = 0;
			j++;
		}
	} 


	public static void main(String[] args){
		int[] arr = makeArr(10,10);

		Arrays.sort(arr);							// O(n lg n)
		System.out.println(Arrays.toString(arr));
		removeDuplicates(arr);						// O(n)
		System.out.println(Arrays.toString(arr));
	}
}