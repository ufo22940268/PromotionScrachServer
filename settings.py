import ignore_me

MODE_DEBUG = 0;
MODE_RELEASE = 1;

#Please check mode before run.
mode = ignore_me.mode;

PAGE_COUNT = 7;
TEST_DATABASE = "test_content.db";
NORMAL_DATABASE = "content.db";
DATABASE_NAME = TEST_DATABASE;

MAX_PAGE_COUNT = 20000;
TEST_PAGE_COUNT = 1000;

def getDbName():
    if mode == MODE_DEBUG:
        return TEST_DATABASE;
    else:
        return NORMAL_DATABASE;
