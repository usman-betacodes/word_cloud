import logging

frag_logger = logging.getLogger("rejected_fragments")
if not frag_logger.handlers:
    frag_logger.setLevel(logging.INFO)
    _handler = logging.FileHandler("rejected_fragments.log", encoding="utf-8")
    _handler.setFormatter(logging.Formatter("%(asctime)s\t%(message)s"))
    frag_logger.addHandler(_handler)
