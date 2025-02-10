import dataclasses


@dataclasses.dataclass
class Mention:
    author: str
    id: str
    run_id: int
    symbol: str
    is_submission: bool = False

    @classmethod
    def from_submission(cls, submission, run_id, symbol):
        return cls(
            author=submission.author,
            id=submission.id,
            run_id=run_id,
            symbol=symbol,
            is_submission=True)
    
    @classmethod
    def from_comment(cls, comment, run_id, symbol):
        return cls(
            author=comment.author,
            id=comment.id,
            run_id=run_id,
            symbol=symbol
        )
