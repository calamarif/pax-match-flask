package com.paxata;

/**
 * Created by callumfinlayson on 11/10/17.
 eg:
 Callum Finlayson Davis
 Callum Davis Finlayson
 Finlayson Callum Davis
 Finlayson Davis Callum
 Davis Finlayson Callum
 Davis Callum Finlayson
 */
public class Permutations
    {
        public static void main(String[] args)
        {
            String str = "Callum Finlayson Davis";

            String[] result = str.split("\\s");
            int n = result.length;
            Permutations permutation = new Permutations();
            permutation.permute(str, 0, n-1);
        }

        /**
         * permutation function
         * @param str string to calculate permutation for
         * @param l starting index
         * @param r end index
         */
        private void permute(String str, int l, int r)
        {
            if (l == r)
                System.out.println(str);
            else
            {
                for (int i = l; i <= r; i++)
                {
                    str = swap(str,l,i);
                    permute(str, l+1, r);
                    str = swap(str,l,i);
                }
            }
        }

        /**
         * Swap Characters at position
         * @param a string value
         * @param i position 1
         * @param j position 2
         * @return swapped string
         */
        public String swap(String a, int i, int j)
        {
            String temp;
            String[] strArray = a.split("\\s");
            temp = strArray[i] ;
            strArray[i] = strArray[j];
            strArray[j] = temp;

            StringBuilder strBuilder = new StringBuilder();
            for (int k = 0; k < strArray.length; k++) {
                strBuilder.append(strArray[k]+" ");
            }
            String newString = strBuilder.toString();

            return String.valueOf(newString);
        }

    }

