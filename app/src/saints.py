from dataclasses import dataclass

from typing import List


@dataclass
class Saint:
    name: str
    picture: str
    traits: List[str]


augustine = Saint(
    name="Augustine of Hippo",
    picture="app/static/SaintAugustineofHippo.jpeg",
    traits="Augustine is known for his deeply personal and introspective writing, particularly in his autobiographical Confessions. He was unafraid to confront his own flaws and failures, and he used his own experiences as a way of exploring and articulating broader theological and philosophical concepts.",
)

dorothy = Saint(
    name="Dorothy Day",
    picture="app/static/DorothyDay.jpeg",
    traits="Day was a radical in the sense that she was deeply committed to transforming society and challenging the status quo. She believed in the possibility of radical change and worked tirelessly to bring it about.",
)

aquinas = Saint(
    name="Thomas Aquinas",
    picture="app/static/ThomasAquinas.jpg",
    traits="Aquinas was known for his ability to synthesize and reconcile seemingly disparate ideas, drawing on a wide range of philosophical and theological traditions. He sought to bring together the insights of ancient Greek philosophy and Christian theology, and his works reflect a deep engagement with both traditions.",
)
