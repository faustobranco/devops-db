def call(int int_Length, boolean bol_SpecialChar){
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
