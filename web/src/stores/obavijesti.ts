import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useObavijestiStore = defineStore('obavijesti', () => {
  const poruka = ref('');
  const tip = ref<'info' | 'greska' | 'uspjeh'>('info');
  const vidljivo = ref(false);

  let timeout: ReturnType<typeof setTimeout>;

  function prikazi(novaPoruka: string, noviTip: 'info' | 'greska' | 'uspjeh' = 'info') {
    poruka.value = novaPoruka;
    tip.value = noviTip;
    vidljivo.value = true;

    clearTimeout(timeout);
    timeout = setTimeout(() => {
      zatvori();
    }, 4000);
  }

  function greska(novaPoruka: string) {
    prikazi(novaPoruka, 'greska');
  }

  function uspjeh(novaPoruka: string) {
    prikazi(novaPoruka, 'uspjeh');
  }

  function zatvori() {
    vidljivo.value = false;
  }

  return { poruka, tip, vidljivo, prikazi, greska, uspjeh, zatvori };
});
