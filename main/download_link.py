class DownloadLink:
    def get_download_link_lc(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2000: 'https://drive.google.com/file/d/1ZmRlAY94Y1h7pAZkrpmBatkfiFCIC5vY/view?usp=drive_link',
            2001: 'https://drive.google.com/file/d/19LzhKVDHr3W51CyT8BUteqn0BThRD8IJ/view?usp=drive_link',
            2002: 'https://drive.google.com/file/d/1V_rRYwYGlAOnkOIj2E3u2TNgejhuXI7u/view?usp=drive_link',
            2003: 'https://drive.google.com/file/d/1D9MDnLNZK01OEyVx3VcTAyRlw4e02hwy/view?usp=drive_link',
            2004: 'https://drive.google.com/file/d/1QVRY8Uv7_FAopkZvjDlMdh7ffE1fMNSm/view?usp=drive_link',
            2005: 'https://drive.google.com/file/d/1azZ1BfSOCmDDn0QrT6RBG6ugSB24kH_G/view?usp=drive_link',
            2006: 'https://drive.google.com/file/d/1l20Q7IgPlURCNF50HmOSw1n9Vv_LGJPG/view?usp=drive_link',
            2007: 'https://drive.google.com/file/d/1LC6XQYRUFhiV8NI5nxE83w2bHlLdVdql/view?usp=drive_link',
            2008: 'https://drive.google.com/file/d/120tSE2fkFYjin8Cr84Un-mAkKWOvxonj/view?usp=drive_link',
            2009: 'https://drive.google.com/file/d/1ETdfttIfrVVscorxMViwY0swXZgotjn5/view?usp=drive_link',
            2010: 'https://drive.google.com/file/d/1oJW8B0A4O_CBrncmuOFaNh3_M7DjyfC9/view?usp=drive_link',
            2011: 'https://drive.google.com/file/d/1TXgoW5OkdALqQ-qMLJFjWIcg9qT3qc9o/view?usp=drive_link',
            2012: 'https://drive.google.com/file/d/1-8Evt-ZUvO975OM2somRqgooGJ0Ue5Wi/view?usp=drive_link',
            2013: 'https://drive.google.com/file/d/1xdqp1zquhqbKrxNtugPPHr6bsjAOylM8/view?usp=drive_link',
            2014: 'https://drive.google.com/file/d/1abo0H8R5NZq7Od1jsYQuTubHNogrD1k1/view?usp=drive_link',
            2015: 'https://drive.google.com/file/d/1gJz4_t8600aCIW_zz14irZD4mSHV_JZG/view?usp=drive_link',
            2016: 'https://drive.google.com/file/d/1rJIDIj4EsZjKbQWdkWd6F1x_PS4zp9fJ/view?usp=drive_link',
            2017: 'https://drive.google.com/file/d/12FWyjAOnz5hXSt653iv5Ec_UhSm1QitT/view?usp=drive_link',
            2018: 'https://drive.google.com/file/d/1A1_oAPwuPRb-jRsgmQJzqIQJg2P39L1r/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/1VrBpeGKV0T1evI3W8fXqrEjFUfN6_XbC/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1aamakGmaO8wU9yAK0FFhD_7hvA7LFb73/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/1VqUQ00napugN2tNQcfh8HJ8ATxaN0Py-/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/14EcSuw8myq0kqZbdQqYUfYV6cQaH-0UW/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/1InkfbyGRPtlIFS3BQt8FojpeWbfOIy4G/view?usp=drive_link',
        }
        
        # Return the download link for the specified year
        return file_links_by_year.get(year)

    def get_download_link_rice(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2000: 'https://drive.google.com/file/d/1lLK2uIjskKF4bocJH4eCb7uB838R7pBb/view?usp=drive_link',
            2001: 'https://drive.google.com/file/d/1mrsRevDnZRBNVtpzTFFu-GZyLlQ3qIFz/view?usp=drive_link',
            2002: 'https://drive.google.com/file/d/18agHjfOKwfwLIf70WuGOfPzta_YT4JeH/view?usp=drive_link',
            2003: 'https://drive.google.com/file/d/19vdIG7FOQ7pKabFfnsSPM7azZHQq75JI/view?usp=drive_link',
            2004: 'https://drive.google.com/file/d/1V6sMGSk9kQgX-GNwBzJ8nbM55TIHgtG7/view?usp=drive_link',
            2005: 'https://drive.google.com/file/d/1QCnDKaUogrMR5Ov0xwzDb5av5d2Mjo-X/view?usp=drive_link',
            2006: 'https://drive.google.com/file/d/1VtkwGgfF9KMZEln_8prnMJDiO_RPbXWy/view?usp=drive_link',
            2007: 'https://drive.google.com/file/d/1HwiJRXFcQFBC5q1u80jHS1_Sxo5-wyDr/view?usp=drive_link',
            2008: 'https://drive.google.com/file/d/1VJFPst3lXEHdlLnF2FPL6VRgss-8xfyy/view?usp=drive_link',
            2009: 'https://drive.google.com/file/d/1vyctQOFsfz4cckULzMsBbIo0soclUL-I/view?usp=drive_link',
            2010: 'https://drive.google.com/file/d/1rZNlWxOjXWQz3KffPxXJ0h3DO79eY63j/view?usp=drive_link',
            2011: 'https://drive.google.com/file/d/119Cf_OkpKy04XL0_BNcEpjmXz7POtr8D/view?usp=drive_link',
            2012: 'https://drive.google.com/file/d/12RLxJ-6HCx9521uNmqGoe-9tFQWhLLSq/view?usp=drive_link',
            2013: 'https://drive.google.com/file/d/1y1t9514s45MsI2qCUO5mFPb_hFNYxQrQ/view?usp=drive_link',
            2014: 'https://drive.google.com/file/d/1gOvd1ThzIyAvV6fhSnLQwiVwYLbAMCuK/view?usp=drive_link',
            2015: 'https://drive.google.com/file/d/1nm_4v9MEnTR6LtHmHfd9dgL7U0nGqoJI/view?usp=drive_link',
            2016: 'https://drive.google.com/file/d/14kWY2tFTgIQ-w98Z021Q7jm-EjMxDZ8F/view?usp=drive_link',
            2017: 'https://drive.google.com/file/d/1muJjjh00gQVWVGgR2bfbQsx4sW3C1ymx/view?usp=drive_link',
            2018: 'https://drive.google.com/file/d/1yRZem6JbCqbVrMLQDGm0stSeynqVOeYe/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/1QJCuGHNs96sHVAu72nn2ohBm7BtxC2QR/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1w0HuWo7DPudMwL0keIwrneSCS0AGzaty/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/18yoiZyOt3dIkaYiSHNCVGONaGhZpQRE8/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/1BIJZmG7m7NI17wCNh5Efa4mvgJUqwp6V/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/18ecI0FO2qOaOqaVDaw89Rc77NL_lktdt/view?usp=drive_link',
        }
        
        # Return the download link for the specified year
        return file_links_by_year.get(year)

    def get_download_link_rubber(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2000: 'https://drive.google.com/file/d/14-YYq-Ka0P181tpeYvDMfloBUFY9QRno/view?usp=drive_link',
            2001: 'https://drive.google.com/file/d/1XPiVkmdwbjeUfDS-II_UlflOlVGtFXCw/view?usp=drive_link',
            2002: 'https://drive.google.com/file/d/1G060Q_HXkiAMshmvS-9MYHDXfjzBXkRw/view?usp=drive_link',
            2003: 'https://drive.google.com/file/d/1fW9EOrix_0d7Au-Vd2jfugwJq_s6iUHI/view?usp=drive_link',
            2004: 'https://drive.google.com/file/d/1hGZ5W3oN8Ryj1A-cWB3WiwNqblrXAJRC/view?usp=drive_link',
            2005: 'https://drive.google.com/file/d/1-rF97pbjG1Mk2Mh77WqwAZu83Owt2M-w/view?usp=drive_link',
            2006: 'https://drive.google.com/file/d/1UKbWRpYbGuI7dsWQosCVF4DrA-vOajqC/view?usp=drive_link',
            2007: 'https://drive.google.com/file/d/1yjZPx-h9JLaYSm14QUJR16TKIkC16ZrY/view?usp=drive_link',
            2008: 'https://drive.google.com/file/d/1P7Q2iUv53QT8WwvnSXQomLlns7X_9vd-/view?usp=drive_link',
            2009: 'https://drive.google.com/file/d/1t94k50DPePxx2ULjN3Osb5akEMnNc-Et/view?usp=drive_link',
            2010: 'https://drive.google.com/file/d/1Unz1M68p0JeaKroVinh8BZzeW_eI9tNM/view?usp=drive_link',
            2011: 'https://drive.google.com/file/d/1TsIKK0LYUfbL-0NspKnML_PDoaC5riqz/view?usp=drive_link',
            2012: 'https://drive.google.com/file/d/1AnxSBRftEgZrnvtuvzmgwTiRXsRGXse5/view?usp=drive_link',
            2013: 'https://drive.google.com/file/d/1HL1BJ-ywZRKqiaF7hztD25cH8Hicswts/view?usp=drive_link',
            2014: 'https://drive.google.com/file/d/1EPsptB5Zx1vradPygbH__sDlhOEHq75c/view?usp=drive_link',
            2015: 'https://drive.google.com/file/d/14K8IZNagaSPu00HfUzyO4mAd8-OyNzw3/view?usp=drive_link',
            2016: 'https://drive.google.com/file/d/1wfWH7q5_8ARNlJQ3Ko3BkT8U-DsHr4O9/view?usp=drive_link',
            2017: 'https://drive.google.com/file/d/1LEJ5BslUcuNpzZdsZOAXBFSPPBdqUWgy/view?usp=drive_link',
            2018: 'https://drive.google.com/file/d/1Un1S-1Wde_LVTW3Jyth3zuJw49RHYJs4/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/1HYPE_wEaDgl1yCdOdzxWEKNbJzFF07iy/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1Lq8SYhvvxVxtkBX5JbygEWhPDCmVO9SH/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/15haAGUKgur9xmqV4fSAu7GqAhbM8zByn/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/13Z7pGx0OCpBE13wFkdXBoLR03ijbtuYA/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/1VWh7DH1O5D7daELtyp20ieg5TkNwII6Z/view?usp=drive_link',
        }
        
        # Return the download link for the specified year
        return file_links_by_year.get(year)
    
    def get_download_link_forestcover(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2000: 'https://drive.google.com/file/d/1ysXImPeuqTD0eqkJ5kuKLxUcpcx0oSIX/view?usp=drive_link',
            2001: 'https://drive.google.com/file/d/1wH43DNZogybevLWrvEwFhif7tQ_luDs2/view?usp=drive_link',
            2002: 'https://drive.google.com/file/d/1bTjzaZzlN91GvtGO8aNd-8Jn8FlZLeq0/view?usp=drive_link',
            2003: 'https://drive.google.com/file/d/18IKguGqLO8KkMpOZlT3oqoEK0BvCzesB/view?usp=drive_link',
            2004: 'https://drive.google.com/file/d/1_LNYYNZSCvXA2UBAAt4USr2bYPpECj1E/view?usp=drive_link',
            2005: 'https://drive.google.com/file/d/1StNzeu_NW7yWOBfs9p5--uAJiT6FJxUW/view?usp=drive_link',
            2006: 'https://drive.google.com/file/d/1om38BuqDK2TDqrk5ShW3J2-Zgr5pfBX9/view?usp=drive_link',
            2007: 'https://drive.google.com/file/d/1295UteCY1YxFlEjRllu0mESNswvMBHV8/view?usp=drive_link',
            2008: 'https://drive.google.com/file/d/1Ym5oRE_KXHzTdJT5SFP25BOSMoV0mIS4/view?usp=drive_link',
            2009: 'https://drive.google.com/file/d/1Kzz4yS03iDd9YBCt8lJThMYeUTz9ROwP/view?usp=drive_link',
            2010: 'https://drive.google.com/file/d/1jm1fL8_s6YDKCQiVV_dixAdL0nrMk9iV/view?usp=drive_link',
            2011: 'https://drive.google.com/file/d/1jX9o7WEs1o_EOyUfg2DCtGhHZ1sOH-mK/view?usp=drive_link',
            2012: 'https://drive.google.com/file/d/1JvGF0lTvZ00Uud8FIJ9wj2cyhGpDyoPV/view?usp=drive_link',
            2013: 'https://drive.google.com/file/d/1nftndoTrMU5y2txY9V1uGm1JtMm6uznu/view?usp=drive_link',
            2014: 'https://drive.google.com/file/d/1JKT5QB7LPMQAnB75OZYRADtLsdaOu6Ub/view?usp=drive_link',
            2015: 'https://drive.google.com/file/d/1l4LclLBs6eG0TNstztW6lPPe9ZWtEy2K/view?usp=drive_link',
            2016: 'https://drive.google.com/file/d/1IoD_MrrZdftK3CUm9oEnUECJzjE3BCj2/view?usp=drive_link',
            2017: 'https://drive.google.com/file/d/1m0rUfq8Ju4qtWNNjU-IecdnLqbvbUT1Q/view?usp=drive_link',
            2018: 'https://drive.google.com/file/d/14JW1OexMghbLRQqqGWX37GsnoNhd3qtt/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/1XDn8HvFXxt8SnRu4usLbRj6EIPiIFrPB/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1XkuJTy7Bg5JCALaJzCLQcODRmUpjiDpW/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/1ngXxRsCZfh3HyPHu3baLIY8wUeen1ciG/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/1-lbIgsoTtThghbK2Jg2zJlHTTsUluxtm/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/18pyF6kHR9x78dKyp4Wgxj0H4olUwZs4O/view?usp=drive_link',
        }
        
        # Return the download link for the specified year
        return file_links_by_year.get(year)

    def get_download_link_fire_hotspot(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2000: 'https://drive.google.com/file/d/1dHLxChpoPbwUk9XdenOZdD7iws0moZ7j/view?usp=drive_link',
            2001: 'https://drive.google.com/file/d/1SZIguE5THXXZudNDxmH_-WIIu8la-eSf/view?usp=drive_link',
            2002: 'https://drive.google.com/file/d/1VKLnP5pYSr7tH_2pwlLGxbIEcso4Mobj/view?usp=drive_link',
            2003: 'https://drive.google.com/file/d/1yUV1-52PF3iBFHsRD0rPkjL4xLdh9geE/view?usp=drive_link',
            2004: 'https://drive.google.com/file/d/1eFW_6o4eoZQVro3dlxh-G053hiuAANaA/view?usp=drive_link',
            2005: 'https://drive.google.com/file/d/1eh0CP9KzAQIQcUcFpdREaVJo1hwWu_AA/view?usp=drive_link',
            2006: 'https://drive.google.com/file/d/11DP10g3jn3b-DP_cV49-Hp-4Y6YNdDg0/view?usp=drive_link',
            2007: 'https://drive.google.com/file/d/1Fqpe_gSUHoMvhgixgoFO-Eheji_3sOod/view?usp=drive_link',
            2008: 'https://drive.google.com/file/d/1esXs7CPeXrDyyKhcOS3t15m3OsHZocHC/view?usp=drive_link',
            2009: 'https://drive.google.com/file/d/1G1k3zsC0-Wj9zuAzz9c_8uHfKgwBC7FG/view?usp=drive_link',
            2010: 'https://drive.google.com/file/d/1idAzO7_181g3JjnNJaBVw2DbY6AOv0v3/view?usp=drive_link',
            2011: 'https://drive.google.com/file/d/1-vAUlaWzf6PiCDiWz5qh6xtPCXPGOnQ2/view?usp=drive_link',
            2012: 'https://drive.google.com/file/d/12wpMsh3NsYZ3PhHI5prfw0bG1dhEm0OP/view?usp=drive_link',
            2013: 'https://drive.google.com/file/d/1XspbHWy7Ihg_hEx1BT04ZWmm_9RNwOV9/view?usp=drive_link',
            2014: 'https://drive.google.com/file/d/1jcaRfRb5GjR3_CLHuB3hBE1TYvIByrTN/view?usp=drive_link',
            2015: 'https://drive.google.com/file/d/1L6kyVIlmjCHlk5rp1vm8hDaaNbK_-U88/view?usp=drive_link',
            2016: 'https://drive.google.com/file/d/1ltGQmirL69caJ7EXhapzxjrXRtiSn29V/view?usp=drive_link',
            2017: 'https://drive.google.com/file/d/1MWE7RWxvrdRDsD8lpM98gNtACegecmdo/view?usp=drive_link',
            2018: 'https://drive.google.com/file/d/1wVSe6fgwAx1tUJW8l8LxKAGqHMHJ_Ils/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/1VbfjoErh11wgw6silkZ9Vya6AvqPDBy4/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1KDGc4Oxn7n5UdndZbZpVdTdD9qHCjEKg/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/1KKMKknY_5TE3Hf-e-J-H3Zb4XqWC5AEX/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/17yVA_v7cnR5yTOw6c0YoXGUvc685HmDC/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/19B5ackk2N4OO_7pBpCrEZCPxS53lIXKg/view?usp=drive_link',
        }
        
        # Return the download link for the specified year
        return file_links_by_year.get(year)

    def get_download_link_gladalert(self, year):
        # Dictionary containing download links mapped by year
        file_links_by_year = {
            2018: 'https://drive.google.com/file/d/1gB8LsqGxORDxvfQNHiMhubTxEo954lZ9/view?usp=drive_link',
            2019: 'https://drive.google.com/file/d/15V-HYiRQ8TcNygRVftojJFj05h0YNDna/view?usp=drive_link',
            2020: 'https://drive.google.com/file/d/1siMrKbajJlyaDCWIsqpxib2lUZRvMVGG/view?usp=drive_link',
            2021: 'https://drive.google.com/file/d/1Mq_wToWGoASq9a82KTVDuoThEC4IIo3P/view?usp=drive_link',
            2022: 'https://drive.google.com/file/d/1ZmGU56nlighJwnp992n2JVg3LKaKbD8w/view?usp=drive_link',
            2023: 'https://drive.google.com/file/d/1welQ6n2Ugb4-QeOzulNYLThrecZzh0vN/view?usp=drive_link',
        }
        # Return the download link for the specified year
        return file_links_by_year.get(year)