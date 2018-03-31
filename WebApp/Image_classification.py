import numpy

class CNN:
    def __init__(layer, unit):
        self.weight = None # Weight Initialize

        pass;

    def feedfoward(self, input_layer):
        '''
        순전파, 입력층(리스트)을 받고 결과를 반환
        '''
        pass;

    def backpropagation(self, inputs, targets):
        '''
        역전파, 입력,타겟 받고 역전파 수행
        '''
        pass;


class layer:
    def set_layer(self, layer, units):
       pass


class pooling(layer):
    def set_pooling(self, pooling_size, stride):
       self.stride = stride
       self.pooling_size = pooling_size


    def feed(input):
        u = []
        for image in input:
            image_channel = [
                [0 for _ in range(len(image))] for _ in range(len(image))
            ]
            for x in range(len(image)-self.pooling_size):
                for y in range(len(image)-self.pooling_size):
                    pool = []
                    for p in range(self.pooling_size):
                        for q in range(self.pooling_size):
                            pool.append(image[x+p][y+q])
                    image_channel[x][y] = max(pool)
            u.append(image_channel)

        return u


class convolution(layer):
    def set_convolution(self, filter, bias, stride):
        self.f = filter  # 필터
        self.b = bias  # 바이어스
        self.stride = stride  # 스트라이드


    def feed(input):
        for image in input:
            new_image = int((length(image)-1)/2)+1
            for line in input:
                if new_image%2 is 0:
                    app = [0 for _ in range(new_image/2)]
                    line = app+line+app
                else:
                    line = [0   for _ in range(int(new_image/2))]+
                     line + [0   for _ in range(rount(new_image/2 + 0.5))]
            new_line = [0 for _ in range(length(line))]
            image = new_line + image + new_line
 #  스트랑이드적용하게바꿔라강준서
        u = []
        for m in filter:
            image_channel = [[0 for _ in length(image)] for _ in length(image)]
            for k in input:
                for x in range(length(image)):
                    for y in range(length(image)):
                        image_channel[x][y]+=sum([
                            sum([
                                    image[x+p][y+q]*self.f[p][q] for q in range(length(self.f))
                                ])
                                for p in range(length(self.f)
                            ])
            u.append(image_channel)
        result= RELU(u)  #렐루 만들어서적용 요망


class fully_connected(layer):
    def set_fc(self, weight, bias):
        pass

class softmax(layer):
    pass
