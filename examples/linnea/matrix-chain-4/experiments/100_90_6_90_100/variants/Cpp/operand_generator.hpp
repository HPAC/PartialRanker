#include <generator/generator.hpp>

template<typename Gen>
decltype(auto) operand_generator(Gen && gen)
{
    auto A = gen.generate({90,100}, generator::property::random{}, generator::shape::not_square{});
    auto B = gen.generate({100,6}, generator::property::random{}, generator::shape::not_square{});
    auto C = gen.generate({6,90}, generator::property::random{}, generator::shape::not_square{});
    auto D = gen.generate({90,100}, generator::property::random{}, generator::shape::not_square{});
    return std::make_tuple(A, B, C, D);
}