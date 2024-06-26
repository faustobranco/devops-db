from devopsdb.pipeline_utils import pipeline_logger

# int_LogLevel, str_LogFormat, str_DateFormat
obj_Logger = pipeline_logger.CreateLogger('TestPipeline', pipeline_logger.LogLevel['debug'].value, '[%(asctime)s] - %(levelname)-8s - [%(name)-12s]: %(message)s', '%H:%M:%S')
obj_Logger.info('Info Log in the test in python.')