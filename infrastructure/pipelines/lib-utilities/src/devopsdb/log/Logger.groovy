/**
 * Class with methods for Log messages in the Pipeline.
 * @author fausto.branco
 * @author https://devops-db.com/
 * @version 1.0
 * @since   2024-05-14
 */

package devopsdb.log

import java.text.SimpleDateFormat

@Singleton(strict = false)
class Logger implements Serializable {

    def obj_Pipeline_Context
    LogFormatter obj_Config_Formatter

    private Logger(obj_Context, LogFormatter obj_Formatter) {
        obj_Pipeline_Context = obj_Context
        obj_Config_Formatter = obj_Formatter
    }

    def debug(String message) {
        logMessage("debug", message)
    }

    def info(String message) {
        logMessage("info", message)
    }

    def error(String message) {
        logMessage("error", message)
    }

    def warning(String message) {
        logMessage("warning", message)
    }

    def logMessage(String level, String message) {
        if (this.obj_Config_Formatter.map_levels[level] <= this.obj_Config_Formatter.int_logLevel) {
            def str_LoggerName = ''
            if (!this.obj_Config_Formatter.str_loggerName.isEmpty()) {
                str_LoggerName = "[${this.obj_Config_Formatter.str_loggerName}]"
            }

            def date = ''
            if (this.obj_Config_Formatter.bol_PrintDate) {
                SimpleDateFormat formatter = new SimpleDateFormat(this.obj_Config_Formatter.str_DateFormat)
                date = formatter.format(new Date())
            }

            obj_Pipeline_Context.echo("${date} [${level.toUpperCase()}] ${str_LoggerName} ${message}")
        }
    }
}