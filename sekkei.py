import yaml
import io
class Config:  
  def __init__(self):
    default_data = {
              'ho_va_ten': 'Nguyễn Đình Hùng',
              'ma_so_sinh_vien': '20131879',
              'ten_file': 'khoosoothunhus.wav',
              'do_dai_frame': 640,
              'nguong_nang_luong': 2
              }   
    # Read YAML file
    try:
      with open("config.yml", 'r') as stream:
        data_loaded = yaml.load(stream)     
    except FileNotFoundError:      
      # Write YAML file
      with io.open('config.yml', 'w', encoding='utf8') as outfile:
          yaml.dump(default_data, outfile, default_flow_style=False, allow_unicode=True)    
    super(Config, self).__setattr__('data', {**default_data, **data_loaded})
     
  def __setattr__(self, k, v):    
    self.data[k] = v    
    with io.open('config.yml', 'w', encoding='utf8') as outfile:
      yaml.dump(self.data, outfile, default_flow_style=False, allow_unicode=True)

  def __getattr__(self, k):      
    try:
      return self.data[k]
    except KeyError:
      raise AttributeError
