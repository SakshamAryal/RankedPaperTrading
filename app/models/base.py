from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    id: Mapped[int] = mapped_column(primary_key=True)
