function updateMoneyFields() {
    const moneyGiveInput = document.getElementById('id_money_give');
    const moneyTakeInput = document.getElementById('id_money_take');
    function updateMoneyTake() {
        var selectedCurrency1 = document.getElementById('currency1').value
        var selectedCurrency2 = document.getElementById('currency2').value
        if (selectedCurrency1 === 'RUB' & selectedCurrency2 === 'UAH' && moneyGiveInput.value > 50000 || selectedCurrency1 === 'RUB' & selectedCurrency2 === 'UAH' && moneyGiveInput.value > 50000){
            const notification_area = document.getElementById('notification_over_get_bank'); notification_area.style.display = 'flex';
            notification_area.innerHTML = " Желательная сумма перевода в одной заявке не более 50 000 тыс. рублей, обмен заявок превышающих 50 000 тыс. обрабатываются через оператора в нашем чате."
            UIkit.notification.closeAll(); 
            UIkit.notification({message: 'Сумма в рублях не может превышать 50тыс. за один  обмен', status: 'danger'});
             moneyTakeInput.value = ""; return;
        }
        if (selectedCurrency1 === 'UAH' & selectedCurrency2 === 'RUB' && moneyGiveInput.value > 50000 || selectedCurrency1 === 'UAH' & selectedCurrency2 === 'RUB' && moneyGiveInput.value > 50000){
            UIkit.notification.closeAll();
            UIkit.notification({message: 'Сумма в гривнах не может превышать 50тыс. за один  обмен', status: 'danger'}); moneyTakeInput.value = "";
            const notification_area = document.getElementById('notification_over_get_bank'); notification_area.style.display = 'flex';
            notification_area.innerHTML = " Желательная сумма перевода в одной заявке не более 50 000 тыс. грн, обмен заявок превышающих 50 000 тыс. обрабатываются через оператора в нашем чате.";
            return;}
        if (moneyGiveInput.value > 1000000){
            UIkit.notification.closeAll()
            UIkit.notification({message: 'Слишком большая сумма', status: 'danger'});
            moneyTakeInput.value = "";
            return;
        }
        const moneyGive = parseFloat(moneyGiveInput.value);
        if (!isNaN(moneyGive)) {
            const currency = price_buy
            const selectedCurrency2 = document.getElementById("currency2").value;
                const moneyTake = moneyGive * currency;
                if (cryptocurrency.includes(selectedCurrency2)){
                    moneyTakeInput.value = moneyTake.toFixed(9);
                    if (window.innerWidth <= 436) {
                        document.getElementById('id_money_take').style.fontSize = '19px' 
                        document.getElementById('id_money_give').style.fontSize = '19px' 
                    }else {
                        document.getElementById('id_money_take').style.fontSize = '27px'
                        document.getElementById('id_money_give').style.fontSize = '27px' 
                    }
                }else {
                    if (selectedCurrency1 === 'BYN' && selectedCurrency2 === 'UAH' || selectedCurrency2 === 'BYN' && selectedCurrency1 === 'UAH'){
                        moneyTakeInput.value = moneyTake.toFixed(3);
                    }else {moneyTakeInput.value = moneyTake.toFixed(0);}
                    if (window.innerWidth <= 436) {
                        document.getElementById('id_money_take').style.fontSize = '27px';
                        document.getElementById('id_money_give').style.fontSize = '27px';
                    }else {
                        document.getElementById('id_money_take').style.fontSize = '35px';
                        document.getElementById('id_money_give').style.fontSize = '35px';
                    }
                }
        }if (moneyTakeInput.value === '0'){
            moneyTakeInput.value = "";
        }
    }
    function updateMoneyGive()
    {
        var selectedCurrency1 = document.getElementById('currency1').value;
        var selectedCurrency2 = document.getElementById('currency2').value;
        if (selectedCurrency1 === 'RUB' & selectedCurrency2 === 'UAH' && moneyGiveInput.value > 50000 || selectedCurrency1 === 'RUB' & selectedCurrency2 === 'UAH' && moneyGiveInput.value > 50000){
            UIkit.notification.closeAll(); UIkit.notification({message: 'Сумма в рублях не может превышать 50тыс. за один  обмен', status: 'danger'});
            const notification_area = document.getElementById('notification_over_get_bank'); notification_area.style.display = 'flex';
            notification_area.innerHTML = " Желательная сумма перевода в одной заявке не более 50 000 тыс. рублей, обмен заявок превышающих 50 000 тыс. обрабатываются через оператора в нашем чате."
            moneyTakeInput.value = "";
            return;
        }
        if (selectedCurrency1 === 'UAH' & selectedCurrency2 === 'RUB' && moneyGiveInput.value > 50000 || selectedCurrency1 === 'UAH' & selectedCurrency2 === 'RUB' && moneyGiveInput.value > 50000){
            const notification_area = document.getElementById('notification_over_get_bank'); notification_area.style.display = 'flex';
            notification_area.innerHTML = " Желательная сумма перевода в одной заявке не более 50 000 тыс. грн, обмен заявок превышающих 50 000 тыс. обрабатываются через оператора в нашем чате."
            UIkit.notification.closeAll(); UIkit.notification({message: 'Сумма в гривнах не может превышать 50тыс. за один  обмен', status: 'danger'});
            moneyTakeInput.value = "";
            return;}
        if (moneyGiveInput.value > 1000000){
            UIkit.notification.closeAll()
            UIkit.notification({message: 'Слишком большая сумма', status: 'danger'});
            moneyTakeInput.value = "";
            return;
        }
        const moneyTake = parseFloat(moneyTakeInput.value);
        if (!isNaN(moneyTake)){
            const currency = price_buy
            const moneyGive = moneyTake / currency;
            if (cryptocurrency.includes(selectedCurrency1)){
                moneyGiveInput.value = moneyGive.toFixed(9);
                if (window.innerWidth <= 436) {
                    document.getElementById('id_money_take').style.fontSize = '19px' 
                    document.getElementById('id_money_give').style.fontSize = '19px' 
                }else {
                    document.getElementById('id_money_take').style.fontSize = '27px'
                    document.getElementById('id_money_give').style.fontSize = '27px' 
                }
            }else {
                if (selectedCurrency1 === 'BYN' && selectedCurrency2 === 'UAH' || selectedCurrency2 === 'BYN' && selectedCurrency1 === 'UAH'){
                    moneyGiveInput.value = moneyGive.toFixed(3);
                }else {moneyGiveInput.value = moneyGive.toFixed(0);}
                if (window.innerWidth <= 436) {
                    document.getElementById('id_money_take').style.fontSize = '27px';
                    document.getElementById('id_money_give').style.fontSize = '27px';
                }else {
                    document.getElementById('id_money_take').style.fontSize = '35px';
                    document.getElementById('id_money_give').style.fontSize = '35px';
                }
            }
        }if (moneyGiveInput.value === '0'){
            moneyGiveInput.value = ""; 
        }
        }
    moneyGiveInput.addEventListener('input', updateMoneyTake);
    moneyTakeInput.addEventListener('input', updateMoneyGive);
}
        
