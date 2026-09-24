def read_library_notice():
    """
    Reads the library notice file and returns its contents.
    """

    try:
        with open(
            "library_notice.txt",
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    except Exception as error:
        return f"Read Error: {error}"


if __name__ == "__main__":
    print(read_library_notice())