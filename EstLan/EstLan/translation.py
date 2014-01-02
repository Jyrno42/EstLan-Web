from EstLan.models import Article, ArticleCategory, CustomPage

from modeltranslation.translator import translator, TranslationOptions


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'short_text', 'content',)


translator.register(Article, ArticleTranslationOptions)


class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(ArticleCategory, ArticleCategoryTranslationOptions)


class CustomPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(CustomPage, CustomPageTranslationOptions)
