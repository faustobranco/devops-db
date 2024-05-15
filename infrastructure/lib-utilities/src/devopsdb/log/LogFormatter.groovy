/**
 * Class with the object with message formatting information.
 * @author fausto.branco
 * @author https://devops-db.com/
 * @version 1.0
 * @since   2024-05-14
 */

package devopsdb.log
@Singleton(strict = false)
class LogFormatter implements Serializable {
    static map_levels = [debug  : 4,
                         info   : 3,
                         warning: 2,
                         error  : 1,
                         none   : 0]
    static String str_DateFormat = ''     // "dd.MM.yyyy - HH:mm:ss.SSS"
    static Boolean bol_PrintDate = true
    static String str_loggerName = ""
    static Integer int_logLevel = 0

    private LogFormatter(logLevel, loggerName, printDate, dateFormat) {
        this.str_DateFormat = dateFormat
        this.bol_PrintDate = printDate
        this.str_loggerName = loggerName
        if (map_levels.containsKey(logLevel)) {
            this.int_logLevel = map_levels[logLevel]
        }
        else {
            this.int_logLevel = 3
        }



    }
}