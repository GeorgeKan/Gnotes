from sqlmodel import Field, SQLModel, Relationship

class PackageTags(SQLModel, table=True):
    package_id: int = Field(default=None, foreign_key='package.id', primary_key=True)
    tag_id: int = Field(default=None, foreign_key='tag.id', primary_key=True)

class TutorialTags(SQLModel, table=True):
    tutorial_id: int = Field(default=None, foreign_key='tutorial.id', primary_key=True)
    tag_id: int = Field(default=None, foreign_key='tag.id', primary_key=True)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str =Field(unique=True)

    tutorials: list["Tutorial"] = Relationship(back_populates='tags', link_model=TutorialTags)
    packages: list["Package"] = Relationship(back_populates='tags', link_model=PackageTags)

class Package(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    desc: str
    url: str
    info: str
    tags: list[Tag] = Relationship(back_populates='packages', link_model=PackageTags)

class Tutorial(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    desc: str
    url: str
    info: str
    tags: list[Tag] = Relationship(back_populates='tutorials', link_model=TutorialTags)