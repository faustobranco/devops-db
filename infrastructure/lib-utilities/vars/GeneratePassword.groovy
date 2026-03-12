def call(int int_Length, boolean bol_SpecialChar){
    /**
     * Method for generating Random passwords, with or without special characters.
     * @param int_Length int - Password length in characters.
     * @param bol_SpecialChar booleal - Does it include special characters?
     * @return String with the generated password.
     * @exception IOException On input error.
     * @see IOException
     */
    def lst_SpecialChar = ['!','@','#','$','%','&']
    def lst_Chars = ['a'..'z', 'A'..'Z', 0..9, '_'].flatten();
    Random rand = new Random(System.currentTimeMillis());
    if (bol_SpecialChar) {
        lst_Chars = lst_Chars + lst_SpecialChar;
    }
    def lst_PasswordChars = (0..int_Length - 1).collect { lst_Chars[rand.nextInt(lst_Chars.size())] };
    def str_RandomPassword = lst_PasswordChars.join('');
    return str_RandomPassword
}
