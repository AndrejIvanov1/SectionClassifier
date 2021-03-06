import re

def format_title(title, verbose=True):
    title = remove_punctuation(title).lower()
    title = classify_title(title, verbose=verbose)

    return title


def remove_punctuation(title):
    return re.sub(r"[/\n?/'\"]", '', title)


"""
  Input: title - (string) title of a section
  Returns: The group of titles the title is in.
           "Other" if title group is not recognized
"""
def classify_title(title, verbose=True):
    if isIntroduction(title):
        return 'Introduction'
    elif isMethods(title):
        return 'Methods'
    elif isResults(title):
        return 'Results'
    elif isDiscussion(title):
        return 'Discussion'
    elif isConclusion(title):
        return 'Conclusion'
    elif isAuthorsContributions(title):
        return 'Authors_Contributions'
    elif isCompetingInterests(title):
        return 'Competing_Interests'
    elif isAbbreviations(title):
        return 'Abbreviations'
    elif isSupporting(title):
        return 'Supporting_Information'
    elif isPrePublicationHistory(title):
        return 'Publication_History'
    elif isCase(title):
        return 'Case'
    else:
        if verbose:
          print("Invalid: {}".format(title))
        return "Other"


def isIntroduction(title):
    return contains(title, 'introduction') or \
           contains(title, 'background')


def isMethods(title):
    return contains(title, 'method') or \
           contains(title, 'material')


def isResults(title):
    return contains(title, 'result') or \
           contains(title, 'finding')


def isDiscussion(title):
    return contains(title, 'discussion')


def isAbbreviations(title):
    return contains(title, 'abbreviation')

def isCase(title):
    return contains(title, 'case')

def isPrePublicationHistory(title):
    return contains(title, 'pre-publication') and \
           contains(title, 'history')


def isConclusion(title):
    return contains(title, 'conclusion') or \
           contains(title, 'concluding') or \
           contains(title, 'summary')


def isAuthorsContributions(title):
    return contains(title, 'author') and \
           contains(title, 'contribution')

def isCompetingInterests(title):
    return contains(title, 'competing') and \
           contains(title, 'interest')

def isSupporting(title):
    return contains(title, 'supporting information') or \
           contains(title, 'supporting material') or \
           (contains(title, 'supplementary') and
            contains(title, 'information'))

def contains(title, word):
    return word in title or \
           (word + 's') in title or \
           (word[:-1] + 'ies') in title

if __name__ == '__main__':
    print(format_title("Author's contributions"))