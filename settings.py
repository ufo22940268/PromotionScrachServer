MODE_DEBUG = 0;
MODE_RELEASE = 1;

#Please check mode before run.
mode = MODE_DEBUG;

PAGE_COUNT = 7;
TEST_DATABASE = "test_content.db";
NORMAL_DATABASE = "content.db";
DATABASE_NAME = TEST_DATABASE;

def getDbName():
    if mode == MODE_DEBUG:
        return TEST_DATABASE;
    else:
        return NORMAL_DATABASE;
