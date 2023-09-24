from sqlalchemy import null
from heartpre.heart_Class import readCategory, NNetConfig, heart_prediction
from heartpre.heart_single_Class import readCategory1, NNetConfig1, heart_prediction1


# 预测函数
def heartPre(test_data):
    if not test_data:
        return null
    cat, cat_to_id = readCategory()
    config = NNetConfig()
    return heart_prediction(cat, config, [test_data])


def heartPre_single(test_data):
    if not test_data:
        return null
    cat, cat_to_id = readCategory1()
    config = NNetConfig1()
    return heart_prediction1(cat, config, [test_data])
