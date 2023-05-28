function updateBankOptions() {
    let cryptocurrency = ['USDT', 'BTC', 'ETH', 'PM'];

    const currencySelect1 = document.getElementById("currency1");
    const currencySelect2 = document.getElementById("currency2");
    const selectedCurrency1 = currencySelect1.value;
    const selectedCurrency2 = currencySelect2.value;
  
    const bankSelect1 = document.getElementById("bank_get");
    const bankSelect2 = document.getElementById("bank_take");
  
    bankSelect1.innerHTML = "";
    bankSelect2.innerHTML = "";
    const notification_area = document.getElementById('notification_over_get_bank');
    notification_area.innerHTML = " ";
    
    if (window.innerWidth > 805) {
    notification_area.style.display = 'none' 
    }
    fetch('api/v1/getBanks') // Replace with the URL of your Django view
      .then(response => response.json())
      .then(banks => {
        const bankOptions1 = banks[selectedCurrency1];
        for (let i = 0; i < bankOptions1.length; i++) {
          const option = document.createElement("option");
            option.text = bankOptions1[i].name;
            option.value = bankOptions1[i].name;
            bankSelect1.add(option);
        }
        const bankOptions2 = banks[selectedCurrency2];
        for (let i = 0; i < bankOptions2.length; i++) {
          const option = document.createElement("option");
            option.text = bankOptions2[i].name;
            option.value = bankOptions2[i].name;
            bankSelect2.add(option);
      }

        if (selectedCurrency1 === selectedCurrency2 || cryptocurrency.includes(selectedCurrency1) & cryptocurrency.includes(selectedCurrency2) || selectedCurrency1 === 'PM' && selectedCurrency2 !== 'UAH' || selectedCurrency2 === 'PM' && selectedCurrency1 !== 'UAH') {
          // if it is, find a different currency to select
          for (let i = 0; i < currencySelect2.options.length; i++) {
              if (currencySelect2.options[i].value !== selectedCurrency1) {
                  currencySelect2.value = currencySelect2.options[i].value;
                  // request(currencySelect2.value, selectedCurrency1);
                  updateMoneyFields();
                  updateBankOptions();
                  break;
              }
          }
        }
    });
    clearInputFields();
    edit_forms();
    request(selectedCurrency1, selectedCurrency2);
}

function edit_forms() {
    let cryptocurrency = ['USDT', 'BTC', 'ETH', 'PM'];
    
    const selectedCurrency1 = document.getElementById("currency1").value;
    const selectedCurrency2 = document.getElementById("currency2").value;

    if (cryptocurrency.includes(selectedCurrency1) || cryptocurrency.includes(selectedCurrency2)){
        if (cryptocurrency.includes(selectedCurrency1) && !cryptocurrency.includes(selectedCurrency2)){
            if (selectedCurrency1 === 'PM'){
                document.getElementById('floationgNumberTaker').style.display = 'flex';
            }else {
                document.getElementById('floationgNumberTaker').style.display = 'none';
            }

            document.getElementById('card_number').style.display = 'none';
            document.getElementById('card_number').value = '';
            
            document.getElementById('binance_wallet_getter').style.display = 'none';
            document.getElementById('binance_wallet_taker').style.display = 'none';
            document.getElementById('binance_wallet_getter').value = '';
            
            document.getElementById('card_number_take').style.display = 'flex';
            document.getElementById('floatingName_take').style.display = 'flex';
        }if (cryptocurrency.includes(selectedCurrency2) && !cryptocurrency.includes(selectedCurrency1)) {

            document.getElementById('floationgNumberTaker').style.display = 'none';
            document.getElementById('card_number_take').style.display = 'none'
            document.getElementById('binance_wallet_getter').style.display = 'none';
            document.getElementById('floatingName_take').style.display = 'none';

            document.getElementById('floatingName_take').value = '';
            document.getElementById('card_number_take').value = '';
            document.getElementById('binance_wallet_getter').value = '';

            document.getElementById('card_number').style.display = 'flex';
            document.getElementById('binance_wallet_taker').style.display = 'flex';

            if (selectedCurrency2 === 'BTC'){
                document.getElementById('binance_wallet_taker').placeholder = 'Номер кошелька Legacy'
                const trcForm = document.getElementById('binance_wallet_taker')
                trcForm.setAttribute('style', 'display: flex; background: url(/static/exchange/images/bitcoin-btc-logo.png) no-repeat right center/contain; padding-right: 49px;');
                return;
            }else{
                document.getElementById('binance_wallet_taker').placeholder = 'Номер кошелька TRC-20'
                const trcForm = document.getElementById('binance_wallet_taker')
                trcForm.setAttribute('style', 'display: flex;');
            }

            if (selectedCurrency2 === 'ETH'){
                document.getElementById('binance_wallet_taker').placeholder = 'Номер кошелька ERC-20'
                const trcForm = document.getElementById('binance_wallet_taker')
                trcForm.setAttribute('style', 'display: flex; background: url(/static/exchange/images/ETH-logo.png) no-repeat right center/contain; padding-right: 49px;');
                return;
            }else{
                document.getElementById('binance_wallet_taker').placeholder = 'Номер кошелька Tether TRC-20'
                const trcForm = document.getElementById('binance_wallet_taker')
                trcForm.setAttribute('style', 'display: flex;');
            }
        }
    }else {

        document.getElementById('binance_wallet_getter').style.display = 'none';
        document.getElementById('binance_wallet_taker').style.display = 'none';
        document.getElementById('floationgNumberTaker').style.display = 'none';
        
        document.getElementById('binance_wallet_getter').value = '';
        document.getElementById('binance_wallet_taker').value = '';
        
        document.getElementById('floatingName_take').style.display = 'flex';
        document.getElementById('card_number').style.display = 'flex';
        document.getElementById('card_number_take').style.display = 'flex';
    }
}