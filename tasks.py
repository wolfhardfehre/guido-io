from invoke import Collection
from lib.tasks import generate

namespace = Collection(
    generate
)
