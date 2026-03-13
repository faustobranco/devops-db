def stepOne() {
    echo "Running step one"
    def str_Password = GeneratePassword(20, true)
    println String.format("New password: %s", str_Password)
    env.NEW_PASSWORD = str_Password

}

return this