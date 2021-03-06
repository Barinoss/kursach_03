import numpy as np
import matplotlib.pyplot as plt


def draw_fft_test(freqs, threshold=50, noise=2):
     if not freqs:
          return False
     for i in range(len(freqs)):
          freqs[i] = int(freqs[i])
     plt.rcParams['figure.figsize'] = [16, 12]
     plt.rcParams.update({'font.size': 18})
     mult = int(max(freqs)/2)
     if mult < 1:
          mult = 1
     dt = 0.5/(max(freqs)+max(freqs)*0.05)/mult #/50  # Разобратсья с частотой дискретизации, диапазоном частот в ффт !!!!!!!!!!!!!!!!!!
     t = np.arange(0, 1, dt)
     f = np.sin(2 * np.pi * freqs[0] * t)
     for i in range(1, len(freqs)):
          f += np.sin(2 * np.pi * freqs[i] * t)


     f += noise*np.random.randn(len(t))
     a = f.tolist()

     f = np.array(a)

     n = len(t)
     fhat = np.fft.fft(f, n)
     PSD = fhat * np.conj(fhat) / n
     freq = (1/(dt*n)) * np.arange(n)
     L = np.arange(1,np.floor(n/2), dtype='int')


     indices = PSD > threshold
     PSDclean = PSD * indices
     fhat = indices * fhat
     ffilt = np.fft.ifft(fhat)

     fig,axs = plt.subplots(4,1)

     plt.sca(axs[0])
     plt.plot(t, f, label='Сигнал з шумами', color='r')
     plt.xlim(t[0], t[-1])
     plt.legend()

     plt.sca(axs[1])
     plt.plot(t, ffilt, label='Відфільтрований сигнал', color='k')
     plt.xlim(t[0], t[-1])
     plt.legend()

     plt.sca(axs[2])
     plt.plot(freq[L], PSD[L], color='c', label="ШПФ")
     plt.xlim(freq[L[0]],freq[L[int(len(L)/mult)-1]])
     plt.legend()

     plt.sca(axs[3])
     plt.plot(freq[L], PSD[L], color='c', label="Шуми")
     plt.plot(freq[L], PSDclean[L], color='k', label='Корисні частоти')
     plt.xlim(freq[L[0]],freq[L[int(len(L)/mult)-1]])
     plt.legend()
     name = str(freqs).replace(' ', '')
     name = str(name+str(threshold)+"+"+str(noise))
     plt.savefig('static/{}.png'.format(name))
     #print(f.tolist())
     return name


def draw_fft(freqs, threshold=50):
     plt.rcParams['figure.figsize'] = [16, 12]
     plt.rcParams.update({'font.size': 18})
     dt = 1/len(freqs)
     t = np.arange(0, 1, dt)


     a = freqs
     f = np.array(a)
     n = len(t)
     fhat = np.fft.fft(f, n)
     PSD = fhat * np.conj(fhat) / n
     freq = (1/(dt*n)) * np.arange(n)
     L = np.arange(1,np.floor(n/2), dtype='int')


     indices = PSD > threshold
     PSDclean = PSD * indices
     psdlist = PSDclean.tolist()
     fhat = indices * fhat
     ffilt = np.fft.ifft(fhat)

     fig,axs = plt.subplots(4,1)

     plt.sca(axs[0])
     plt.plot(t[:len(f)], f, label='Сигнал з шумами', color='r')
     plt.xlim(t[0], t[-1])
     plt.legend()

     plt.sca(axs[1])
     plt.plot(t, ffilt, label='Відфільтрований сигнал', color='k')
     plt.xlim(t[0], t[-1])
     plt.legend()

     plt.sca(axs[2])
     plt.plot(freq[L], PSD[L], color='c', label="ШПФ")
     plt.xlim(freq[L[0]],freq[L[-1]])
     plt.legend()

     plt.sca(axs[3])
     plt.plot(freq[L], PSD[L], color='c', label="Шуми")
     plt.plot(freq[L], PSDclean[L], color='k', label='Корисні частоти')
     plt.xlim(freq[L[0]],freq[L[-1]])
     plt.legend()
     name = str(freqs[0])
     plt.savefig('static/{}.png'.format(name))
     return name, ffilt.tolist()


if __name__ == '__main__':
    draw_fft_test([50, 120, 200, 155])