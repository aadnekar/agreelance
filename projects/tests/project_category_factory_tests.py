import pytest

from projects.factories.project_category_factory import ProjectCategoryFactory


@pytest.mark.parametrize(
    "category_name_expected",
    [
        ("Cleaning"),
        ("Painting"),
        ("Gardening"),
        ("Cleaning")
    ]
)
@pytest.mark.django_db
def test_first_category_name_is_correct(category_name_expected):
    """
    The ProjectCategoryFactory creates categories Cleaning, Painting
    and Gardening iteratively when the factory is called.
    """
    category = ProjectCategoryFactory()

    assert category.name == category_name_expected

