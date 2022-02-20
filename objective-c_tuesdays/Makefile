TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : $(TMP)/blog-pretty.xml


.PHONY : clean
clean :
	-rm -rf $(TMP)


$(TMP)/blog-pretty.xml : data/blog.xml | $$(dir $$@)
	XMLLINT_INDENT='    ' xmllint --format $< > $@

$(TMP)/blog-08-09-2020-pretty.xml : data/blog-08-09-2020.xml | $$(dir $$@)
	XMLLINT_INDENT='    ' xmllint --format $< > $@

$(TMP) :
	mkdir -p $@
