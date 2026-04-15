import logging
import os

CHINESE_TIME_FORMAT = "%Y年%m月%d日%H时%M分%S秒"
LOG_FORMAT = "[%(levelname)s] %(asctime)s%(msecs)03d毫秒：%(message)s"
THIRD_PARTY_LOG_LEVELS = {
    "telethon": logging.WARNING,
}

PG_DSN = os.getenv(
    "PG_DSN",
    "postgresql://postgres:postgres@127.0.0.1:5432/postgres",
)

PG_CRYPTO_KEY = os.getenv("PG_CRYPTO_KEY", "replace-me-with-a-real-secret")

BSC_RPC_LIST = os.getenv(
    "BSC_RPC_LIST",
    "https://bsc-mainnet.core.chainstack.com/4c5f6dc42d6e967e0f65879f217038e8,"
    "https://bsc-mainnet.core.chainstack.com/5c45f03f08b62159f5143efebd0f0468,"
    "https://bsc-mainnet.core.chainstack.com/0309bc72a7152bacd83f95a955f80205",
).split(",")

BSC_WSS_URL = os.getenv(
    "BSC_WSS_URL",
    "wss://bsc-mainnet.core.chainstack.com/ws/5c45f03f08b62159f5143efebd0f0468",
)

FREEDOM_ROUTER_ADDRESS = os.getenv(
    "FREEDOM_ROUTER_ADDRESS", "0x08e365CfaAEd969312Ed3d2477a63026885012FE"
)

DEFAULT_SWAP_CONFIG = {
    "buy_slippage": 0.2,
    "buy_gas": 0.5,
    "buy_bundletip": 0.0001,
    "sell_slippage": 0.2,
    "sell_gas": 0.5,
    "sell_bundletip": 0.0001,
}

DEFAULT_LIMIT_CONFIG_ITEM = {
    "change_percent": None,
    "sell": None,
    "executed": False,
}

DEFAULT_LIMIT_CONFIG = []

DEFAULT_IMAGE_MATCH_CONFIG = {
    "enabled": False,
    "check_self_imgs": True,
    "check_ref_imgs": False,
    "use_ocr": False,
    "use_similarity": False,
    "similarity_threshold": 0.8,
}

DEFAULT_HANDLE_CATEGORIES = [
    {
        "platform": "x",
        "categories": [
            {
                "category": "co_founder",
                "handles": [
                    {
                        "handle": "cz_binance",
                        "enabled": False,
                        "remark": "币安创始人，前 CEO",
                    },
                    {
                        "handle": "heyibinance",
                        "enabled": False,
                        "remark": "币安联合创始人",
                    },
                    {
                        "handle": "nina_rong",
                        "enabled": False,
                        "remark": "BNB Chain 增长负责人",
                    },
                    {
                        "handle": "cz_square",
                        "enabled": False,
                        "remark": "CZ 的 Square 账号",
                    },
                    {
                        "handle": "heyi_square",
                        "enabled": False,
                        "remark": "何一的 Square 账号",
                    },
                ],
            },
            {
                "category": "binance_affiliate",
                "handles": [
                    {
                        "handle": "BinanceAcademy",
                        "enabled": False,
                        "remark": "币安学院",
                    },
                    {
                        "handle": "BinanceResearch",
                        "enabled": False,
                        "remark": "币安研究院",
                    },
                    {"handle": "BinanceAfrica", "enabled": False, "remark": "币安非洲"},
                    {
                        "handle": "BinanceAngels",
                        "enabled": False,
                        "remark": "币安天使计划",
                    },
                    {
                        "handle": "Binance_AUS",
                        "enabled": False,
                        "remark": "币安澳大利亚",
                    },
                    {"handle": "BinanceBrasil", "enabled": False, "remark": "币安巴西"},
                    {
                        "handle": "BinanceArabic",
                        "enabled": False,
                        "remark": "币安阿拉伯语",
                    },
                    {"handle": "BinanceArg", "enabled": False, "remark": "币安阿根廷"},
                    {"handle": "BinancePk", "enabled": False, "remark": "币安巴基斯坦"},
                    {
                        "handle": "binance_vietnam",
                        "enabled": False,
                        "remark": "币安越南",
                    },
                    {
                        "handle": "binanceafrique",
                        "enabled": False,
                        "remark": "币安非洲法语区",
                    },
                    {
                        "handle": "BinanceUkraine",
                        "enabled": False,
                        "remark": "币安乌克兰",
                    },
                    {
                        "handle": "_RichardTeng",
                        "enabled": False,
                        "remark": "币安现任 CEO",
                    },
                    {"handle": "BinanceWallet", "enabled": False, "remark": "币安钱包"},
                    {
                        "handle": "BinanceFutures",
                        "enabled": False,
                        "remark": "币安合约",
                    },
                    {"handle": "binancezh", "enabled": False, "remark": "币安中文"},
                    {
                        "handle": "Binance_intern",
                        "enabled": False,
                        "remark": "币安实习生账号",
                    },
                    {"handle": "BinanceVIP", "enabled": False, "remark": "币安 VIP"},
                    {
                        "handle": "BinanceDesi",
                        "enabled": False,
                        "remark": "币安印度市场",
                    },
                    {
                        "handle": "BinanceItalian",
                        "enabled": False,
                        "remark": "币安意大利",
                    },
                    {"handle": "LeBinanceFR", "enabled": False, "remark": "币安法国"},
                    {
                        "handle": "cis_binance",
                        "enabled": False,
                        "remark": "币安独联体地区",
                    },
                    {"handle": "BinanceES", "enabled": False, "remark": "币安西语"},
                    {"handle": "Binance_NZL", "enabled": False, "remark": "币安新西兰"},
                    {"handle": "_BinanceJapan", "enabled": False, "remark": "币安日本"},
                    {"handle": "Binance_TH_", "enabled": False, "remark": "币安泰国"},
                    {
                        "handle": "BinanceMoonbix",
                        "enabled": False,
                        "remark": "币安 Moonbix",
                    },
                    {"handle": "BinancePoland", "enabled": False, "remark": "币安波兰"},
                    {"handle": "BinanceForIN", "enabled": False, "remark": "币安印度"},
                    {
                        "handle": "BNBCHAIN",
                        "enabled": False,
                        "remark": "BNB Chain 官方",
                    },
                    {
                        "handle": "BNBChainDevs",
                        "enabled": False,
                        "remark": "BNB Chain 开发者",
                    },
                    {
                        "handle": "BNBCHAINZH",
                        "enabled": False,
                        "remark": "BNB Chain 中文",
                    },
                    {
                        "handle": "BNBChainLatAm",
                        "enabled": False,
                        "remark": "BNB Chain 拉美",
                    },
                    {
                        "handle": "BNBCHAINKR",
                        "enabled": False,
                        "remark": "BNB Chain 韩国",
                    },
                    {"handle": "Binance", "enabled": False, "remark": "币安全球主账号"},
                ],
            },
        ],
    },
]

parsed_data = {
    "tweet_id": "1734567890123456789",
    "platform": "x",
    "delay_ms": 0,
    "tweet_type": "reply",
    "handle": "@current_user",
    "ref_handle": "@target_author",
    "ref_nickname": "风光摄影师",
    "ref_bio": "记录山海与沿途风景 🏔️🌊",
    "content": "",
    "reply": "拍得真好看！",
    "replied_to": "分享我今天拍的风景照。",
    "quote": "",
    "quoted": "",
    "retweet": "",
    "self_imgs": ["https://example.com/1.jpg"],
    "ref_imgs": ["https://example.com/2.jpg"],
}

match_positions_template = {
    "match_positions": {
        "ref_handle": False,
        "ref_nickname": False,
        "ref_bio": False,
        "content": True,
        "reply": True,
        "replied_to": False,
        "quote": False,
        "quoted": False,
        "retweet": False,
    }
}


def setup_logging() -> None:
    for logger_name, level in THIRD_PARTY_LOG_LEVELS.items():
        logging.getLogger(logger_name).setLevel(level)

    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.INFO,
        datefmt=CHINESE_TIME_FORMAT,
    )
