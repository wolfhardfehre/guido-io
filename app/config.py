import logging

LOG_LEVEL = logging.INFO
FORMAT = '%(asctime)s.%(msecs)03d %(levelname)5s %(process)d ---' \
         '[%(name)22s][%(lineno)4d] %(filename)-20s : %(message)s'
logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)
