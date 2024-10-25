TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : $(TMP)/objective-c_tuesdays.stamp.txt


.PHONY : clean
clean :
	-rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf ./.venv


.PHONY : prettify
prettify : $(TMP)/blog-08-09-2020-pretty.xml $(TMP)/blog-pretty.xml


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


$(TMP)/blog-pretty.xml : data/blog.xml | $$(dir $$@)
	XMLLINT_INDENT='    ' xmllint --format $< > $@


$(TMP)/blog-08-09-2020-pretty.xml : data/blog-08-09-2020.xml | $$(dir $$@)
	XMLLINT_INDENT='    ' xmllint --format $< > $@


$(TMP)/objective-c_tuesdays.stamp.txt : $(TMP)/blog-pretty.xml uv.lock | $$(dir $$@)
	uv run main.py --brief $< tmp/objective-c_tuesdays
	date > $@


$(TMP)/uv-sync.stamp.txt : uv.lock | $$(dir $$@)
	uv sync --frozen
	date > $@


$(TMP)/ :
	mkdir -p $@
