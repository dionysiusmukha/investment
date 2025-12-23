from Client import MyEntity_rep_DB, FilteredSortedDB, FilteredSortedFile


def create_filtered_repo(repo):
    if isinstance(repo, MyEntity_rep_DB):
        return FilteredSortedDB(repo)
    else:
        return FilteredSortedFile(repo)
