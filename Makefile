cleanup:
	rm ./data/._amex_*
	rm ./data/._visa_*
	rm ./data/._visa2_*
	rm ./data/._debit_*

run:
	@python main.py $(YEAR) $(MONTH) > ./out/$(YEAR)-$(MONTH).out