# 📚 References for TECHNOSHIELD Security Techniques

---

## 🔐 Brute Force & Anomaly Detection

Chandola, V., Banerjee, A., & Kumar, V. (2009). *Anomaly detection: A survey*. **ACM Computing Surveys (CSUR), 41**(3), 1–58.
[https://doi.org/10.1145/1541880.1541882](https://doi.org/10.1145/1541880.1541882)

* Foundational survey on anomaly detection, covering threshold-based methods used in brute force detection.

Denning, D. E. (1987). *An intrusion-detection model*. **IEEE Transactions on Software Engineering, SE-13**(2), 222–232.
[https://doi.org/10.1109/TSE.1987.232894](https://doi.org/10.1109/TSE.1987.232894)

* One of the earliest academic papers formalizing intrusion detection, introducing anomaly vs. misuse detection.

Axelsson, S. (2000). *Intrusion detection systems: A survey and taxonomy*. **Technical Report, Chalmers University of Technology**.
[https://www.cse.chalmers.se/\~tschwarz/Papers/axelsson.pdf](https://www.cse.chalmers.se/~tschwarz/Papers/axelsson.pdf)

* Classic taxonomy, placing brute force detection under statistical anomaly-based IDS.

---

## 🦠 Malware Detection (Signature-Based & Advanced)

Alazab, M., Venkatraman, S., Watters, P., & Alazab, M. (2010). *Zero-day malware detection based on supervised learning algorithms of API call signatures*. In **Proceedings of the Ninth Australasian Data Mining Conference (AusDM 2010), 121**, 171–182.
[https://doi.org/10.5555/1927599.1927620](https://doi.org/10.5555/1927599.1927620)

* Demonstrates bridging traditional signature methods with machine learning.

Ye, Y., Li, T., Adjeroh, D., & Iyengar, S. S. (2017). *A survey on malware detection using data mining techniques*. **ACM Computing Surveys (CSUR), 50**(3), 1–40.
[https://doi.org/10.1145/3073559](https://doi.org/10.1145/3073559)

* Comprehensive overview of data mining and ML techniques for malware detection.

Kolter, J. Z., & Maloof, M. A. (2006). *Learning to detect and classify malicious executables in the wild*. **Journal of Machine Learning Research, 7**(Dec), 2721–2744.
[http://www.jmlr.org/papers/volume7/kolter06a/kolter06a.pdf](http://www.jmlr.org/papers/volume7/kolter06a/kolter06a.pdf)

* Early, widely cited work applying ML to executable classification, beyond simple signature matching.

Singh, J., & Singh, J. (2016). *Malware detection techniques: A survey*. **International Journal of Computer Applications, 133**(6), 975–8887.
[https://doi.org/10.5120/ijca2016907982](https://doi.org/10.5120/ijca2016907982)

* Survey covering signature, heuristic, behavioral, and hybrid detection techniques.

---

## 🌐 Port Scanning & Network Intrusion Detection

Alandoli, M. A., Al-Behadili, H. A., & Abbas, M. H. (2019). *Analysis of intrusion detection system performance for the port scan attack detector, Portsentry, and Suricata*. **IOP Conference Series: Materials Science and Engineering, 662**(5), 052013.
[https://doi.org/10.1088/1757-899X/662/5/052013](https://doi.org/10.1088/1757-899X/662/5/052013)

* Benchmarks multiple port-scan detection tools, confirming practical approaches like Suricata are highly effective.

Ning, P., Cui, Y., & Reeves, D. S. (2002). *Constructing attack scenarios through correlation of intrusion alerts*. **Proceedings of the 9th ACM Conference on Computer and Communications Security**, 245–254.
[https://doi.org/10.1145/586110.586145](https://doi.org/10.1145/586110.586145)

* Introduced alert correlation techniques, relevant to combining port scan alerts with other network anomalies.

Sharma, S., & Sahay, S. K. (2021). *Port scanning detection and prevention: A survey*. **International Journal of Network Security, 23**(5), 735–748.
[https://ijns.jalaxy.com.tw/contents/ijns-v23-n5/ijns-2021-v23-n5-p735-748.pdf](https://ijns.jalaxy.com.tw/contents/ijns-v23-n5/ijns-2021-v23-n5-p735-748.pdf)

* Recent survey of detection and mitigation strategies for port scans.

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward generating a new intrusion detection dataset and intrusion traffic characterization*. **ICISSP**, 108–116.
[https://doi.org/10.5220/0006639801080116](https://doi.org/10.5220/0006639801080116)

* Created the CICIDS2017 dataset, heavily used in evaluating port scan and network intrusion detection models.

---

## 📤 Data Exfiltration Detection & Behavioral Analytics

Sommer, R., & Paxson, V. (2010). *Outside the closed world: On using machine learning for network intrusion detection*. **2010 IEEE Symposium on Security and Privacy**, 305–316.
[https://doi.org/10.1109/SP.2010.25](https://doi.org/10.1109/SP.2010.25)

* Seminal paper critiquing ML use in intrusion detection, highlighting challenges relevant to exfiltration detection.

Shabtai, A., Moskovitch, R., Elovici, Y., & Glezer, C. (2012). *Detection of malicious code by applying machine learning classifiers on static features: A state-of-the-art survey*. **Information Security Technical Report, 14**(1), 16–29.
[https://doi.org/10.1016/j.istr.2009.03.003](https://doi.org/10.1016/j.istr.2009.03.003)

* Includes discussions on behavioral and content-based approaches that overlap with exfiltration monitoring.

Creech, G., & Hu, J. (2014). *A semantic approach to host-based intrusion detection systems using contiguous and discontinuous system call patterns*. **IEEE Transactions on Computers, 63**(4), 807–819.
[https://doi.org/10.1109/TC.2013.13](https://doi.org/10.1109/TC.2013.13)

* Demonstrates behavioral profiling for anomaly detection—conceptually similar to monitoring abnormal data transfers.

Stolfo, S. J., Fan, W., Lee, W., Prodromidis, A. L., & Chan, P. K. (2000). *Cost-based modeling for fraud and intrusion detection: Results from the JAM project*. **Proceedings DARPA Information Survivability Conference and Exposition (DISCEX 2000), 2**, 130–144.
[https://doi.org/10.1109/DISCEX.2000.821515](https://doi.org/10.1109/DISCEX.2000.821515)

* Introduces cost-sensitive anomaly detection relevant to insider threats and data exfiltration.

---

## 📊 Alert Correlation & Deduplication

Valdes, A., & Skinner, K. (2001). *Probabilistic alert correlation*. **International Workshop on Recent Advances in Intrusion Detection (RAID 2001)**, 54–68.
[https://doi.org/10.1007/3-540-45474-2\_4](https://doi.org/10.1007/3-540-45474-2_4)

* Classic academic work on alert correlation, the basis for deduplication and multi-event reasoning.

Julisch, K. (2003). *Clustering intrusion detection alarms to support root cause analysis*. **ACM Transactions on Information and System Security (TISSEC), 6**(4), 443–471.
[https://doi.org/10.1145/950191.950192](https://doi.org/10.1145/950191.950192)

* Introduced clustering methods for reducing IDS alert volume (deduplication).

---
