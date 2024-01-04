from app.components.words_learning import WordFlashcard


def open_word_flashcard(language):
    """Open a word flashcard.

        This function opens a word flashcard with the specified language.

        Args:
            language (str): The language of the word flashcard.
        """
    app = WordFlashcard(language)
    app.mainloop()
