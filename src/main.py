from textnode import TextNode, TextType


def main():
    node = TextNode("This is some link", TextType.LINK, "htttps://google.com")
    print(node)


if __name__ == "__main__":
    main()
