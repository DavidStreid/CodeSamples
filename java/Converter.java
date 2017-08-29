import java.util.*;

/*
	Class with methods to convert String representations of Roman numberals to their corresponding decimal numbers and vice-versa

	$ javac Converter.java  && java Converter
*/
public class Converter{
	private static Map<Character,Integer> map = new HashMap<Character,Integer>();
	static {
		map.put('I',1);
		map.put('V',5);
		map.put('X',10);
		map.put('L',50);
		map.put('C',100);
		map.put('D',500);
		map.put('M',1000);
	}

	/*
		Converts romanNumberal to int representation

		input (String): romanNumber
		output (int): decimal representation
	*/
	public static int romanToDecimal(String romanNumber){
		if(romanNumber == null || romanNumber == "" ){
			return 0;
		}

		int i = 0;			// Pointer to characters of input
		int dec = 0;		// Decimal value of input

		int curr,next;

		// Process characters in input in groups of twos and add to dec
		while(i<romanNumber.length()-1){
			curr = map.get(romanNumber.charAt(i));
			next = map.get(romanNumber.charAt(i+1));
			if(curr < next){
				dec += next-curr;
				i += 2;
			}
			else {
				dec += curr;
				i += 1;
			}
		}

		// Evaluate input's last character, which should be evaluated individually
		if(i==romanNumber.length()-1){
			dec += map.get(romanNumber.charAt(i));
		}
		return dec;
	}
	/*
		Create Stack of roman numerals in the order they should appear (1000,900,500,400,100,90,50,40,10,9,5,4,1)
	*/
	public static List<String> createRomans(){
		
		List<String> romans = new ArrayList<String>(Arrays.asList("M","CM","D","CD","C","XC","L","XL","X","IX","V", "IV","I"));
		return romans;
	}

	/*
		Takes either a 1 or 2 character romanNumeral string and returns its corresponding integer value
		Input (String): c
		Output(Integer)
	*/	
	public static Integer getStackCharacter(String c){
		// 
		if(c.length()>1){
			return map.get(c.charAt(1)) - map.get(c.charAt(0));
		}
		else {
			return map.get(c.charAt(0));
		}
	}

	/*
		Converts integer to roman numeral representation

		Input(int) : decimalNumber
		Output(Stirng): roman numeral represntation
	*/
	public static String decimalToRoman(int decimalNumber){
		StringBuilder sb = new StringBuilder();
		List<String> romans = createRomans();		// Creates stack of Roman numerals in order they should appear
		// Subtract roman numerals from decimal number until it reaches 0
		while(decimalNumber > 0){
			String curr = romans.get(0);

			// Subtract current roman numeral if it is bigger than decimalNumber
			if(decimalNumber - getStackCharacter(curr) >= 0){
				sb.append(curr);
				decimalNumber -= getStackCharacter(curr);
			}
			// If not, move to next roman numeral
			else {
				romans.remove(0);
			}
		}
		return sb.toString();
	}

	/*
		Tester method checking equality and printing to stdOut if not equal
	*/	
	public static void assertEquals(Object obj1, Object obj2){
		if(!obj1.equals(obj2)){
			System.out.println(String.format("TEST FAIL: actual %s not equal to expected %s",
				obj1.toString(),obj2.toString()));
		}
	}

	/*
		Runs test cases
	*/
	public static void runTests(){
		int[] decimals = {0,1,5,8,9,13,14,38,39,40,48,49,88,89,90,99,398,400,899,999,2999};
		String[] romans = {"","I","V","VIII","IX","XIII","XIV","XXXVIII","XXXIX","XL","XLVIII","XLIX","LXXXVIII","LXXXIX","XC","XCIX","CCCXCVIII","CD","DCCCXCIX","CMXCIX","MMCMXCIX"};

		// Test romanToDecimal
		for(int i = 0; i<decimals.length; i++){
			assertEquals(romanToDecimal(romans[i]),decimals[i]);
			assertEquals(decimalToRoman(decimals[i]),romans[i]);
		}
	}

	public static void main(String[] args){
		runTests();
	}
}